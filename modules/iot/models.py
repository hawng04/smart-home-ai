# modules/iot/models.py
from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer) # Ở đây làm đơn giản, chưa cần mapping relationship phức tạp
    name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)
    mqtt_topic = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), default="OFF")

class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True) # Tên nhân vật (VD: Em gái Hà Nội)
    prompt = Column(Text)