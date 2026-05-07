# modules/iot/router.py
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import engine
from modules.iot.models import Device

# Nhúng thư viện MQTT
import paho.mqtt.publish as publish

router = APIRouter(prefix="/api/devices", tags=["IoT Devices"])

# Cấu hình MQTT Broker đám mây
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# --- CÁC KHUÔN MẪU DỮ LIỆU ---
class DeviceControl(BaseModel):
    device_id: int
    action: str

class DeviceCreate(BaseModel):
    name: str
    device_type: str

# --- 1. LẤY DANH SÁCH THIẾT BỊ ---
@router.get("/")
def get_devices():
    db = Session(bind=engine)
    devices = db.query(Device).all()
    db.close()
    return devices

# --- 2. ĐIỀU KHIỂN BẬT/TẮT (ĐÃ LẮP BỘ ĐÀM MQTT) ---
@router.post("/control")
def control_device(req: DeviceControl):
    db = Session(bind=engine)
    device = db.query(Device).filter(Device.id == req.device_id).first()
    if device:
        # Cập nhật Database
        device.status = req.action
        db.commit()
        
        # PHÁT SÓNG MQTT KHI BẤM NÚT BẰNG TAY
        topic = f"xiaozhi_home/device/{req.device_id}"
        try:
            publish.single(topic, payload=req.action, hostname=MQTT_BROKER, port=MQTT_PORT)
            print(f"📡 Nút bấm thủ công -> Topic: {topic} | Lệnh: {req.action}")
        except Exception as e:
            print(f"Lỗi gửi MQTT thủ công: {e}")
            
    db.close()
    return {"message": "Đã điều khiển thiết bị"}

# --- 3. THÊM THIẾT BỊ MỚI ---
@router.post("/")
def add_device(req: DeviceCreate):
    db = Session(bind=engine)
    new_dev = Device(name=req.name, device_type=req.device_type, status="OFF", mqtt_topic="temp")
    db.add(new_dev)
    db.flush() 
    new_dev.mqtt_topic = f"xiaozhi_home/device/{new_dev.id}"
    db.commit()
    db.close()
    return {"message": "Đã thêm thiết bị mới"}

# --- 4. XÓA THIẾT BỊ ---
@router.delete("/{device_id}")
def delete_device(device_id: int):
    db = Session(bind=engine)
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
    db.close()
    return {"message": "Đã xóa thiết bị"}