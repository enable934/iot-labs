import random
import time
import json
import paho.mqtt.client as mqtt

# Функція для симуляції даних сенсора вологості (%)
previous_value = 50.0  # Початкове значення
def generate_humidity():
    global previous_value
    delta = random.uniform(-5.0, 5.0)
    previous_value = round(max(0.0, min(100.0, previous_value + delta)), 2) 
    return previous_value

# MQTT клієнт для публікації даних
client = mqtt.Client(client_id="humidity_sensor_simulation_client", protocol=mqtt.MQTTv5)
client.connect("mqtt_broker", 1883, 60)

# Симуляція зчитування даних з сенсорів
if __name__ == "__main__":
    for _ in range(10):  # Симулюємо 10 вимірювань
        data = {
            "value": generate_humidity(),
            "sensor_type": "humidity"
        }
        client.publish("sensor/data", json.dumps(data))
        print(f"Дані відправлено: {data}")
        time.sleep(1)  # Затримка 1 секунда між вимірюваннями