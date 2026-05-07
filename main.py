# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.database import engine, Base
from modules.iot.router import router as iot_router
from modules.ai.router import router as ai_router # Import thêm Router của phần AI

# Tạo thư mục chứa file MP3 trước khi server khởi động (nếu chưa có)
os.makedirs("static/audio", exist_ok=True)

# Lệnh này yêu cầu SQLAlchemy tạo các bảng trong DB nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Home Server")

# Cấu hình CORS để Frontend (React) gọi được API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Mở cửa cho Frontend truy cập vào thư mục static để tải file nhạc MP3
app.mount("/static", StaticFiles(directory="static"), name="static")

# Nhúng các Router vào App
app.include_router(iot_router)
app.include_router(ai_router) # Khai báo cho app biết về AI Router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)