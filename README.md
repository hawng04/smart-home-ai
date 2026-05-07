## Công nghệ sử dụng (Tech Stack)

### Backend (Python)
- **Framework:** FastAPI (High performance API).
- **AI/LLM:** Google Gemini 2.5 Flash API.
- **Database:** MySQL + SQLAlchemy (ORM).
- **IoT/MQTT:** `paho-mqtt` kết nối với HiveMQ Broker.
- **Audio/Media:** `gTTS` (Text-to-Speech), thư viện `urllib` & `re` (Cào dữ liệu YouTube ID).

### Frontend (React)
- **Library:** ReactJS (Vite / Create React App).
- **Voice API:** `react-speech-recognition`.
- **HTTP Client:** `axios`.
- **UI:** CSS module (Responsive, Dark Mode UI).

---

## Hướng dẫn Cài đặt & Khởi chạy

### 1. Yêu cầu hệ thống (Prerequisites)
- [Node.js](https://nodejs.org/) (Phiên bản 16.x trở lên)
- [Python](https://www.python.org/) (Phiên bản 3.8 trở lên)
- [XAMPP](https://www.apachefriends.org/) (Để chạy MySQL Server)
- API Key của **Google Gemini** (Lấy miễn phí tại [Google AI Studio](https://aistudio.google.com/))

### 2. Thiết lập Cơ sở dữ liệu (Database)
1. Mở XAMPP Control Panel, khởi động **MySQL**.
2. Truy cập `http://localhost/phpmyadmin`.
3. Tạo một database mới với tên: `smart_home_db`.

### 3. Cài đặt Backend (FastAPI)
Mở terminal tại thư mục backend, chạy các lệnh sau:
```bash
# Tạo môi trường ảo (Virtual Environment)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
.\venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install fastapi uvicorn sqlalchemy pymysql paho-mqtt google-genai gtts

# Cấu hình API Key
# Mở file modules/ai/router.py và dán Gemini API Key của bạn vào dòng GEMINI_API_KEY.

# Khởi động Server (Hệ thống sẽ tự động tạo các bảng SQL)
python main.py