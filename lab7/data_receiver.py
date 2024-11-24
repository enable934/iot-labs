import paho.mqtt.client as mqtt
import json
import os
import time

# Функція, яка обробляє отримані дані та виводить їх у консоль
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        print(f"Отримані оброблені дані від шлюзу: {data}")
    except json.JSONDecodeError:
        print("Не вдалося декодувати повідомлення:", msg.payload)

# Функція для обробки підключення
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Підключення до MQTT брокера успішне")
        client.subscribe("iot/devices/data")
        print("Підписано на тему 'iot/devices/data'")
    else:
        print(f"Помилка підключення. Код результату: {rc}")

# Налаштування MQTT клієнта
data_receiver_client = mqtt.Client(client_id="data_receiver_client", protocol=mqtt.MQTTv311)
data_receiver_client.on_connect = on_connect
data_receiver_client.on_message = on_message

print("Підключення до MQTT брокера для отримання оброблених даних...")
data_receiver_client.connect("mqtt_broker", 1883, 60)

data_receiver_client.loop_forever()