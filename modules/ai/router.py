# modules/ai/router.py
import urllib.request
import urllib.parse
import os
import time
import re
import traceback
import os
from dotenv import load_dotenv

# Tự động tìm và đọc file .env
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS

from google import genai
from google.genai import types
import paho.mqtt.publish as publish

from sqlalchemy.orm import Session
from core.database import engine
from modules.iot.models import Device, Persona

# --- THƯ VIỆN MỚI ĐỂ TÌM YOUTUBE ---
from youtubesearchpython import VideosSearch

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------------------------------------
# --------------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)
router = APIRouter(prefix="/api/ai", tags=["AI Chat"])

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

class ChatRequest(BaseModel):
    text: str
    persona_id: int

class PersonaCreate(BaseModel):
    name: str
    prompt: str

@router.get("/personas")
def get_personas():
    db = Session(bind=engine)
    personas = db.query(Persona).all()
    if not personas:
        default_persona = Persona(name="Em gái xứ Nghệ", prompt="ĐỊNH DANH: Bạn là trợ lý...")
        db.add(default_persona)
        db.commit()
        db.refresh(default_persona)
        personas = [default_persona]
    db.close()
    return personas

@router.post("/personas")
def add_persona(req: PersonaCreate):
    db = Session(bind=engine)
    new_persona = Persona(name=req.name, prompt=req.prompt)
    db.add(new_persona)
    db.commit()
    db.close()
    return {"message": "Đã thêm nhân cách mới"}

@router.delete("/personas/{persona_id}")
def delete_persona(persona_id: int):
    db = Session(bind=engine)
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if persona:
        db.delete(persona)
        db.commit()
    db.close()
    return {"message": "Đã xóa nhân cách"}

@router.post("/chat")
def chat_with_bot(req: ChatRequest):
    user_text = req.text
    db = Session(bind=engine)
    
    try:
        persona = db.query(Persona).filter(Persona.id == req.persona_id).first()
        persona_prompt = persona.prompt if persona else "Bạn là một AI quản gia."

        now = datetime.now()
        current_time_str = f"{now.hour}:{now.minute} ngày {now.day}/{now.month}/{now.year}"
        
        devices = db.query(Device).all()
        device_list_str = "\n".join([f"- ID: {d.id} | Tên: {d.name} | Trạng thái: {d.status}" for d in devices])

        dynamic_instruction = persona_prompt + f"""
        [YÊU CẦU KỸ THUẬT BẮT BUỘC]
        1. Trả lời cực kỳ NGẮN GỌN. Không dùng markdown.
        2. Thời gian: {current_time_str}. Thiết bị: {device_list_str}
        3. NẾU bật/tắt thiết bị: BẮT BUỘC chèn [ACTION:ID_THIẾT_BỊ:TRẠNG_THÁI] vào cuối.
        4. NẾU mở nhạc: BẮT BUỘC chèn [MUSIC:Tên_bài_hát] vào cuối.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=user_text,
            config=types.GenerateContentConfig(system_instruction=dynamic_instruction),
        )
        bot_reply = response.text.strip()
        
        # --- BÓC TÁCH VÀ TÌM ID YOUTUBE THẬT ---
        # --- BÓC TÁCH VÀ TÌM ID YOUTUBE THẬT (DÙNG NATIVE PYTHON) ---
        music_match = re.search(r'\[MUSIC:(.+?)\]', bot_reply, re.IGNORECASE)
        song_name = None
        youtube_id = None
        if music_match:
            song_name = music_match.group(1).strip()
            bot_reply = re.sub(r'\[MUSIC:.+?\]', '', bot_reply, flags=re.IGNORECASE).strip()
            
            # Bí kíp tự cào dữ liệu YouTube không cần thư viện ngoài
            try:
                query = urllib.parse.quote(song_name)
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}").read().decode()
                video_ids = re.findall(r"watch\?v=(\S{11})", html)
                if video_ids:
                    youtube_id = video_ids[0]
                    print(f"✅ Đã tìm thấy ID bài hát: {youtube_id}")
            except Exception as e:
                print("🚨 Lỗi tìm YouTube:", e)
        
        matches = re.finditer(r'\[ACTION:(\d+):(ON|OFF)\]', bot_reply, re.IGNORECASE)
        action_taken = False
        
        for match in matches:
            device_id = int(match.group(1))
            action = match.group(2).upper()
            device = db.query(Device).filter(Device.id == device_id).first()
            if device:
                device.status = action
                action_taken = True
                try:
                    publish.single(f"xiaozhi_home/device/{device_id}", payload=action, hostname=MQTT_BROKER, port=MQTT_PORT)
                except:
                    pass
        if action_taken:
            db.commit()
            
        clean_reply = re.sub(r'\[ACTION:\d+:(ON|OFF)\]', '', bot_reply, flags=re.IGNORECASE).strip()

    except Exception as e:
        traceback.print_exc()
        clean_reply = "Hệ thống đang bảo trì."
        song_name = None
        youtube_id = None
    finally:
        db.close()

    tts = gTTS(text=clean_reply, lang='vi')
    filepath = os.path.join("static", "audio", "reply.mp3")
    tts.save(filepath)

    return {
        "reply": clean_reply,
        "audio_url": f"http://localhost:8000/static/audio/reply.mp3?v={int(time.time())}",
        "song_name": song_name,
        "youtube_id": youtube_id # <-- Gửi ID thật xuống Web
    }