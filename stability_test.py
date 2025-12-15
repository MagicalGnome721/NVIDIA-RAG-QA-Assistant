import time
import pandas as pd
import os
import random
from datetime import datetime
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# --- 1. CẤU HÌNH ---
ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
print(f"--- Đang kết nối Ollama tại: {ollama_url} ---")

Settings.llm = Ollama(model="llama3", base_url=ollama_url, request_timeout=300.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# --- 2. LOAD DỮ LIỆU ---
print("--- Đang nạp dữ liệu vào VRAM... ---")
if not os.path.exists("./data"):
    print("LỖI: Thiếu folder data!")
    exit()

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# --- 3. BỘ DỮ LIỆU STRESS TEST (Nhân bản câu hỏi) ---
# Chúng ta dùng 5 câu hỏi gốc và nhân bản lên để chạy vòng lặp
base_questions = [
    "Vị trí này yêu cầu bằng cấp gì?",
    "Kinh nghiệm làm việc với GPU có quan trọng không?",
    "Nhiệm vụ chính của SWQA là gì?",
    "CUDA là bắt buộc hay điểm cộng?",
    "Làm sao để ứng viên nổi bật hơn người khác?"
]

# Tạo 50 lượt test ngẫu nhiên
total_runs = 50
test_queue = [random.choice(base_questions) for _ in range(total_runs)]

results = []
print(f"\n🔥 BẮT ĐẦU STRESS TEST ({total_runs} lượt) TRÊN RTX 3060 🔥")
print("Hãy theo dõi cửa sổ nvidia-smi để xem nhiệt độ!")

# --- 4. VÒNG LẶP TRA TẤN ---
start_stress_time = time.time()

for i, question in enumerate(test_queue):
    iter_start = time.time()
    
    # Gửi request
    try:
        response = query_engine.query(question)
        status = "PASS"
        output_len = len(str(response))
    except Exception as e:
        status = f"FAIL: {str(e)}"
        output_len = 0
    
    iter_end = time.time()
    duration = iter_end - iter_start
    
    # Tính tốc độ
    est_speed = (output_len / 4) / duration if duration > 0 else 0
    
    # Log ra màn hình cho ngầu
    print(f"[{i+1}/{total_runs}] {status} | Time: {duration:.2f}s | Speed: {est_speed:.1f} t/s | Len: {output_len}")
    
    results.append({
        "Iteration": i + 1,
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Question": question,
        "Status": status,
        "Latency (s)": round(duration, 2),
        "Tokens/Sec (Est)": round(est_speed, 2)
    })

total_duration = time.time() - start_stress_time
print(f"\n✅ STRESS TEST HOÀN TẤT SAU {total_duration:.2f} GIÂY")

# --- 5. XUẤT BÁO CÁO ---
df = pd.DataFrame(results)
filename = f"stress_test_report_{int(time.time())}.csv"
df.to_csv(filename, index=False)
print(f"Đã lưu log chi tiết vào: {filename}")