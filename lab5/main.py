import random
import time

# Функція для симуляції даних сенсора температури (°C)
def generate_temperature():
    return round(random.uniform(15.0, 30.0), 2)

# Функція для симуляції даних сенсора вологості (%)
def generate_humidity():
    return round(random.uniform(30.0, 70.0), 2)

# Симуляція зчитування даних з сенсорів
if __name__ == "__main__":
    for _ in range(10):  # Симулюємо 10 вимірювань
        temperature = generate_temperature()
        humidity = generate_humidity()
        print(f"Температура: {temperature}°C, Вологість: {humidity}%")
        time.sleep(1)  # Затримка 1 секунда між вимірюваннями