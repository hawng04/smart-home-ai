from core.mqtt_client import mqtt_service

# Giả lập Database trạng thái thiết bị
devices_db = {
    "light_livingroom": {"name": "Đèn phòng khách", "status": "OFF"},
    "fan_bedroom": {"name": "Quạt phòng ngủ", "status": "OFF"}
}

def get_device_status(device_id: str):
    return devices_db.get(device_id)

def control_device(device_id: str, action: str):
    """
    Hàm này nhận lệnh từ API hoặc từ AI Module
    """
    if device_id in devices_db:
        # 1. Cập nhật DB
        devices_db[device_id]["status"] = action.upper()
        
        # 2. Gửi lệnh MQTT xuống thiết bị thật
        # Topic ví dụ: home/livingroom/light/set
        topic = f"home/{device_id}/set"
        mqtt_service.publish(topic, action.upper())
        
        return True, f"Đã chuyển {devices_db[device_id]['name']} sang {action}"
    return False, "Không tìm thấy thiết bị"