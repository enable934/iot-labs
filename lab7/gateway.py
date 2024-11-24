import paho.mqtt.client as mqtt
import time
import json
import os

# Функція, яка обробляє отримані дані та виводить їх у консоль
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(f"Дані отримано на шлюзі: {data}")
    # Відправка отриманих даних на інший IoT пристрій
    response_data = {
        "device": "gateway",
        "status": "processed",
        "original_data": data
    }
    client.publish("iot/devices/data", json.dumps(response_data))
    print(f"Відправлено відповідь на інший пристрій: {response_data}")

# Функція для обробки підключення
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Підключення до MQTT брокера успішне")
        client.subscribe("sensor/data")
    else:
        print(f"Помилка підключення. Код результату: {rc}")

# Налаштування MQTT клієнта
gateway_client = mqtt.Client(client_id="gateway_client", protocol=mqtt.MQTTv5)
gateway_client.on_connect = on_connect
gateway_client.on_message = on_message

print("Підключення до MQTT брокера для отримання даних...")
gateway_client.connect("mqtt_broker", 1883, 60)

gateway_client.loop_forever()