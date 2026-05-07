import paho.mqtt.client as mqtt

# Cấu hình MQTT Broker
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # Bắt đầu chạy ngầm
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"📡 [MQTT] Đã kết nối tới Broker! Mã: {rc}")

    def publish(self, topic: str, message: str):
        print(f"📤 [MQTT] Gửi '{message}' tới topic '{topic}'")
        self.client.publish(topic, message)

# Tạo 1 instance duy nhất để dùng chung cho cả app (Singleton)
mqtt_service = MQTTService()