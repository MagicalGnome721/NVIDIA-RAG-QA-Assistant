# File: test_rag_qa.py

import pytest
import time
from app import rag_query # Giả sử hàm query RAG chính của bạn nằm trong app.py

# --- Test Data: Map từ TEST_MATRIX.md ---
# Các câu hỏi chức năng quan trọng
TEST_QUESTIONS = [
    ("FN-001", "Vị trí này yêu cầu bằng cấp gì?", "Bachelor's degree or equivalent practical experience"),
    ("FN-002", "Giá cổ phiếu Tesla hôm nay?", "không tìm thấy thông tin liên quan"),
    ("FN-003", "Kinh nghiệm làm việc với GPU có quan trọng không?", "là một điểm cộng lớn"),
]

# --- Functional Test Harness ---
@pytest.mark.parametrize("test_id, question, expected_keyword", TEST_QUESTIONS)
def test_functional_accuracy(test_id, question, expected_keyword):
    """
    Kiểm tra độ chính xác chức năng (Functional Accuracy) và Negative Test.
    """
    print(f"\n--- Running {test_id}: {question}")
    
    # 1. Thực hiện truy vấn RAG
    response, source_nodes, latency = rag_query(question) 
    
    # 2. ASSERTS (Logic PASS/FAIL)
    
    # Assertion 1: Câu trả lời không được rỗng
    assert response is not None and len(response) > 5, "Lỗi: Câu trả lời RAG bị rỗng hoặc quá ngắn."
    
    # Assertion 2: Kiểm tra keyword mong đợi (Nội dung chính xác)
    # Chúng ta dùng lower() để kiểm tra không phân biệt chữ hoa/thường
    assert expected_keyword.lower() in response.lower(), \
        f"Lỗi {test_id}: Thiếu từ khóa '{expected_keyword}' trong câu trả lời."
        
    # Assertion 3 (Tùy chọn): Kiểm tra tốc độ cơ bản (Dưới 3 giây)
    assert latency < 3.0, f"Lỗi: Latency quá cao: {latency:.2f}s (Cần < 3s)."
    
    print(f"PASS ({test_id}): {response[:100]}...")


# --- Performance Test Harness (Kiểm tra điều kiện đơn giản) ---
def test_performance_baseline():
    """
    Kiểm tra tốc độ tối thiểu (Baseline Performance) theo PF-001.
    """
    question = "Mô tả trách nhiệm chính của vị trí SWQA?"
    
    start_time = time.time()
    response, _, _ = rag_query(question)
    end_time = time.time()
    
    duration = end_time - start_time
    
    # Pass Criteria từ TEST_MATRIX.md: Latency < 1.5s cho câu hỏi trung bình
    assert duration < 1.5, f"Lỗi PF-001: Latency quá chậm: {duration:.2f}s (Cần < 1.5s)."

# Lưu ý: Cần đảm bảo hàm 'rag_query' trả về (response, source_nodes, latency)