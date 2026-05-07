from modules.iot import service as iot_service # <-- Gọi thẳng thằng IoT vào đây

def process_text_command(text: str):
    """
    Logic xử lý ngôn ngữ tự nhiên (NLP) đơn giản
    """
    text = text.lower()
    
    # Logic "Ngu ngơ" (Hardcode) - Sau này bạn thay bằng AI Model xịn ở đây
    if "bật đèn" in text and "phòng khách" in text:
        # Gọi module IoT thực thi ngay
        success, msg = iot_service.control_device("light_livingroom", "ON")
        return {
            "reply_text": "Ok, đã bật đèn phòng khách cho bạn.",
            "action_performed": "TURN_ON_LIGHT",
            "iot_result": msg
        }
        
    elif "tắt đèn" in text:
         success, msg = iot_service.control_device("light_livingroom", "OFF")
         return {
            "reply_text": "Đã tắt đèn rồi nhé.",
            "action_performed": "TURN_OFF_LIGHT",
             "iot_result": msg
        }
    
    return {
        "reply_text": "Xin lỗi, tôi chưa hiểu ý bạn.",
        "action_performed": None
    }