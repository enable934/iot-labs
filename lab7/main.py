import random
import time
import json
import paho.mqtt.client as mqtt

# Функція для симуляції даних сенсора температури (°C)
def generate_temperature():
    return round(random.uniform(15.0, 30.0), 2)

# Функція для симуляції даних сенсора вологості (%)
def generate_humidity():
    return round(random.uniform(30.0, 70.0), 2)

# MQTT клієнт для публікації даних
client = mqtt.Client(client_id="sensor_simulation_client", protocol=mqtt.MQTTv5)
client.connect("mqtt_broker", 1883, 60)

# Симуляція зчитування даних з сенсорів
if __name__ == "__main__":
    for _ in range(10):  # Симулюємо 10 вимірювань
        data = {
            "temperature": generate_temperature(),
            "humidity": generate_humidity()
        }
        client.publish("sensor/data", json.dumps(data))
        print(f"Дані відправлено: {data}")
        time.sleep(1)  # Затримка 1 секунда між вимірюваннями