import paho.mqtt.client as mqtt
import json
import os
import time
import matplotlib.pyplot as plt
import pandas as pd

# Змінні для зберігання даних
data_list = []
# Функція, яка обробляє отримані дані та виводить їх у консоль
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        print(f"Отримані оброблені дані від шлюзу: {data}")
        data_list.append(data)

        # Якщо отримано 5 повідомлень, візуалізуємо їх
        if len(data_list) % 5:
            visualize_data(data_list)
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

# Функція для візуалізації даних
def visualize_data(data_list):
    temperature_data = []
    humidity_data = []
    timestamps = []

    for data in data_list:
        device_data = data.get("original_data", {}).get("data", {})
        if "temperature" in device_data:
            temperature_data.append(device_data["temperature"])
            humidity_data.append(None)  # Для підтримки однакової довжини списків
        elif "humidity" in device_data:
            humidity_data.append(device_data["humidity"])
            temperature_data.append(None)  # Для підтримки однакової довжини списків
        timestamps.append(time.strftime('%Y-%m-%d %H:%M:%S'))

    # Створюємо DataFrame для візуалізації
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Temperature': temperature_data,
        'Humidity': humidity_data
    })
    df.set_index('Timestamp', inplace=True)

    # Побудова графіку
    plt.figure(figsize=(10, 5))
    if df['Temperature'].notna().any():
        df['Temperature'].dropna().plot(label='Temperature (°C)', marker='o')
    if df['Humidity'].notna().any():
        df['Humidity'].dropna().plot(label='Humidity (%)', marker='o')
    
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Temperature and Humidity Data Visualization')
    plt.legend()
    plt.grid(True)

    # Збереження графіку у папку
    plt.savefig(f"visualizations/visualization_{time.strftime('%Y%m%d_%H%M%S')}.png")
    plt.close()
    print("Графік збережено у папку 'visualizations'")

# Налаштування MQTT клієнта
data_receiver_client = mqtt.Client(client_id="data_receiver_client", protocol=mqtt.MQTTv311)
data_receiver_client.on_connect = on_connect
data_receiver_client.on_message = on_message

print("Підключення до MQTT брокера для отримання оброблених даних...")
data_receiver_client.connect("mqtt_broker", 1883, 60)

data_receiver_client.loop_forever()