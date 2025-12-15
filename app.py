import os
import chainlit as cl
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer

# =======================================================
# 1. CẤU HÌNH HỆ THỐNG AI
# =======================================================

# Lấy địa chỉ Ollama (Mặc định localhost)
ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
print(f"--- Đang kết nối tới Ollama tại: {ollama_url} ---")

Settings.llm = Ollama(
    model="llama3",
    base_url=ollama_url,
    request_timeout=300.0,
    system_prompt="""
    Bạn là Trợ lý Tuyển dụng ảo của NVIDIA.
    NHIỆM VỤ:
    1. Trả lời các câu hỏi của ứng viên dựa trên JD (Job Description) được cung cấp.
    2. Nhấn mạnh vào yêu cầu về: GPU, CUDA, Testing và Automation.
    3. Luôn tỏ ra chuyên nghiệp, ngắn gọn và khuyến khích ứng viên nộp CV.
    Nếu không có thông tin trong JD, hãy nói: "Thông tin này không được đề cập trong bản mô tả công việc."
    """
)

# Cấu hình Model nhúng (Embedding)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# =======================================================
# 2. KHỞI ĐỘNG HỆ THỐNG
# =======================================================

@cl.on_chat_start
async def start():
    # Sửa 1: Tên Bot chuyên nghiệp hơn
    msg = cl.Message(content="🚀 **NVIDIA HR Assistant đang khởi động...**")
    await msg.send()

    # Kiểm tra folder data
    if not os.path.exists("./data") or not os.listdir("./data"):
        await cl.Message(content="⚠️ Folder `data` đang trống hoặc không tồn tại. Hãy copy file JD vào đó.").send()
        return

    try:
        # Đọc dữ liệu từ folder
        documents = SimpleDirectoryReader("./data").load_data()
        
        # Tạo Index
        index = VectorStoreIndex.from_documents(documents)
        
        # Tạo bộ nhớ
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

        # Tạo Chat Engine
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=Settings.llm.system_prompt,
            similarity_top_k=3
        )
        
        # Lưu session
        cl.user_session.set("chat_engine", chat_engine)

        # Sửa 2: Câu lệnh chuẩn, không bị lỗi cú pháp
        msg.content = f"✅ **Sẵn sàng!**\nĐã kết nối Ollama tại `{ollama_url}`.\nĐã học xong JD vị trí SWQA. Mời bạn đặt câu hỏi về công việc!"
        await msg.update()
        
    except Exception as e:
        error_msg = f"❌ Lỗi khởi động: {str(e)}"
        if "Connection refused" in str(e):
            error_msg += "\n\n💡 Gợi ý: Kiểm tra xem Ollama đã bật chưa?"
        await cl.Message(content=error_msg).send()

# =======================================================
# 3. XỬ LÝ TIN NHẮN
# =======================================================

@cl.on_message
async def main(message: cl.Message):
    chat_engine = cl.user_session.get("chat_engine")
    
    if not chat_engine:
        await cl.Message(content="⚠️ Hệ thống chưa sẵn sàng. Hãy F5 lại trang.").send()
        return

    msg = cl.Message(content="")
    
    # Gọi AI trả lời
    response = chat_engine.stream_chat(message.content)
    
    # Hiện chữ dần dần
    for token in response.response_gen:
        await msg.stream_token(token)

    await msg.send()