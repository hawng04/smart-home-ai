# modules/iot/schemas.py
from pydantic import BaseModel

# Schema để trả dữ liệu ra (GET)
class DeviceResponse(BaseModel):
    id: int
    name: str
    device_type: str
    mqtt_topic: str
    status: str

    class Config:
        from_attributes = True

# Schema để nhận lệnh từ AI/User (POST) - Hồi nãy bạn thiếu cái này nè!
class DeviceCommand(BaseModel):
    device_id: int
    action: str