import random
import time
import json
import paho.mqtt.client as mqtt

# Функція для симуляції даних сенсора температури (°C)
previous_value = 20.0  # Початкове значення
def generate_temperature():
    global previous_value
    delta = random.uniform(-3.0, 2.0)
    previous_value = round(max(-10.0, min(40.0, previous_value + delta)), 2) 
    return previous_value

# MQTT клієнт для публікації даних
client = mqtt.Client(client_id="temperature_sensor_simulation_client", protocol=mqtt.MQTTv5)
client.connect("mqtt_broker", 1883, 60)

# Симуляція зчитування даних з сенсорів
if __name__ == "__main__":
    for _ in range(10):  # Симулюємо 10 вимірювань
        data = {
            "value": generate_temperature(),
            "sensor_type": "temperature"
        }
        client.publish("sensor/data", json.dumps(data))
        print(f"Дані відправлено: {data}")
        time.sleep(1)  # Затримка 1 секунда між вимірюваннями