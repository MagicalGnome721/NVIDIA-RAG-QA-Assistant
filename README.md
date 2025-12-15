# 🚀 NVIDIA Recruitment Assistant (RAG) - Automated QA & Performance Benchmarking

> **Project Goal:** Xây dựng một trợ lý ảo RAG sử dụng **Llama 3 (Quantized Int4)** để trả lời các câu hỏi chuyên sâu về Job Description (JD) của NVIDIA, đồng thời phát triển bộ công cụ tự động kiểm thử hiệu năng và độ ổn định (Stress Testing) trên nền tảng **RTX 3060** cục bộ.

## 🎯 1. Mục tiêu và Giải pháp Kỹ thuật (Problem-Solving)

### 1.1. Giải pháp Hạ tầng (Infrastructure Solution)
| Vấn đề ban đầu (The Problem) | Giải pháp Kỹ thuật (The Solution) | Kết quả (The Result) |
| :--- | :--- | :--- |
| ❌ **Lỗi `SIGBUS`** và bottleneck VRAM do chạy trên Docker (WSL2). | Di chuyển toàn bộ hạ tầng từ Docker sang **Native Windows** (Bare-metal execution). | Khắc phục hoàn toàn lỗi crash, giảm **Latency** và tăng hiệu năng GPU trực tiếp lên **~20%** nhờ tận dụng tối đa CUDA cores. |
| ❌ Thiếu công cụ đo lường hiệu năng chuyên biệt cho AI RAG. | Xây dựng script **`stability_test.py`** tùy chỉnh bằng Python, kết hợp đo lường **Tokens/Sec** và giám sát **Latency**. | Đảm bảo tính ổn định và cung cấp dữ liệu định lượng (Quantifiable Data) cho báo cáo QA. |

### 1.2. Kiến trúc (Architecture)
* **Mô hình (Model):** Llama 3 (8B Instruct - Quantized Int4)
* **Hạ tầng AI:** Ollama, LlamaIndex, LangChain
* **Giao diện:** Chainlit (Web UI)
* **Database:** ChromaDB/FAISS (Vector Store)

## 🧪 2. Phương pháp Kiểm thử (QA Methodology)

Dự án này tập trung vào hai loại kiểm thử chính:

1.  **Functional Testing:** Xác minh độ chính xác của câu trả lời RAG so với tài liệu JD gốc.
2.  **Performance & Stress Testing (Key QA Focus):**
    * Sử dụng script `stability_test.py` để chạy **50+ chu kỳ liên tục** nhằm mô phỏng tải nặng (high-load traffic).
    * Giám sát **VRAM, nhiệt độ GPU** (qua `nvidia-smi`) và phân tích dữ liệu hiệu năng bằng Pandas.
3.  **Continuous Integration (CI):** Thiết lập **GitHub Actions** để tự động chạy Test Harness sau mỗi lần commit.
## 📊 3. Kết quả Benchmark (Trên NVIDIA RTX 3060 12GB)

| Metric | Chi tiết | Kết quả | Insight |
| :--- | :--- | :--- | :--- |
| **Stability Test** | Số chu kỳ thành công/Tổng số chu kỳ (50 Iterations). | **100% PASS** | Hệ thống duy trì độ ổn định tuyệt đối dưới tải nặng và không ghi nhận lỗi. |
| **Peak Throughput** | Tốc độ xử lý tối đa khi tạo câu trả lời dài. | **76.74 Tokens/sec** | Đạt hiệu suất tối ưu trên phần cứng tiêu dùng. |
| **Average Latency** | Thời gian phản hồi trung bình cho mỗi truy vấn. | **0.87 giây** | Đảm bảo trải nghiệm tương tác gần như thời gian thực (Real-time). |
| **Caching/Throttling** | So sánh hiệu năng đầu tiên và cuối cùng. | **Tăng tốc 40%** (10 câu cuối > 10 câu đầu) | **Không bị quá nhiệt.** Cho thấy việc caching và tối ưu bộ nhớ hoạt động hiệu quả khi chạy dài. |

***(Gắn hình ảnh biểu đồ Line Chart của bạn vào đây)***

## 🛠 4. Hướng dẫn cài đặt và chạy (Quick Start)

### Yêu cầu Hệ thống
* NVIDIA GPU (RTX 3060 hoặc tương đương)
* Python 3.10+
* Đã cài đặt Ollama

### Các bước thực hiện
1. Clone Repository về máy:
   ```bash
   git clone [https://github.com/MagicalGnome721/NVIDIA-RAG-QA-Assistant.git](https://github.com/MagicalGnome721/NVIDIA-RAG-QA-Assistant.git)
   cd NVIDIA-RAG-QA-Assistant
Cài đặt các thư viện cần thiết:

Bash

pip install -r requirements.txt
Tải và chạy mô hình Llama 3 (qua Ollama):

Bash

ollama pull llama3
Chạy ứng dụng Chatbot:

Bash

chainlit run app.py -w
Chạy bộ Stress Test (trong Terminal khác):

Bash

python stability_test.py

<img width="623" height="261" alt="image" src="https://github.com/user-attachments/assets/49b61e83-8d93-424d-9e8b-998313f4aefa" />
