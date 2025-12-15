import time
import pandas as pd
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. CẤU HÌNH (Y hệt app.py để đảm bảo môi trường test giống thật)
print("--- KHỞI TẠO MÔI TRƯỜNG TEST ---")
Settings.llm = Ollama(model="llama3", request_timeout=300.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# 2. LOAD DỮ LIỆU
print("--- ĐANG LOAD DỮ LIỆU TỪ ./data ---")
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# 3. BỘ TEST CASE (Test Matrix)
test_cases = [
    "Vị trí này yêu cầu bằng cấp gì?",
    "NVIDIA cần kỹ năng lập trình nào?",
    "Làm sao để nổi bật khi ứng tuyển vị trí này?",  # Câu hỏi dài để test khả năng tổng hợp
    "CUDA là điểm cộng hay bắt buộc?",
    "Mô tả trách nhiệm chính của vị trí SWQA?"
]

results = []

print("\n--- BẮT ĐẦU BENCHMARK TRÊN RTX 3060 ---")
print(f"Running {len(test_cases)} test cases...\n")

# 4. CHẠY TEST VÀ ĐO HIỆU NĂNG
for i, question in enumerate(test_cases):
    print(f"Test #{i+1}: {question}")
    
    start_time = time.time()
    response = query_engine.query(question)
    end_time = time.time()
    
    duration = end_time - start_time
    char_count = len(str(response))
    tokens_per_sec_approx = (char_count / 4) / duration # Ước lượng thô (1 token ~ 4 chars)
    
    print(f" -> Time: {duration:.2f}s | Output: {char_count} chars")
    
    results.append({
        "Test Case": question,
        "Status": "PASS" if char_count > 0 else "FAIL",
        "Latency (s)": round(duration, 2),
        "Est. Speed (Tokens/s)": round(tokens_per_sec_approx, 2)
    })

# 5. XUẤT BÁO CÁO (Report)
df = pd.DataFrame(results)
print("\n=== KẾT QUẢ BENCHMARK ===")
print(df)

# Lưu ra file Excel để đính kèm CV hoặc show trong video
df.to_csv("nvidia_rtx3060_benchmark_report.csv", index=False)
print("\n✅ Đã lưu báo cáo test vào 'nvidia_rtx3060_benchmark_report.csv'")