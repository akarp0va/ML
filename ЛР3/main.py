import sqlite3
import random
from datetime import datetime

# Функция для создания базы данных и таблиц
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS WeatherConditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        is_raining BOOLEAN
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SoilMoisture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moisture_level REAL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS IrrigationSettings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_of_day TEXT,
        irrigation_amount REAL
    );
    ''')

    conn.commit()
    conn.close()

# Функция для генерации случайных данных и их добавления в базу данных
def generate_random_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Случайные данные о погоде
    temperature = round(random.uniform(0, 35), 1)  # Температура от 10 до 35 градусов
    humidity = round(random.uniform(0, 100), 1)    # Влажность от 20% до 100%
    is_raining = random.choice([True, False])       # Идёт дождь или нет

    cursor.execute('INSERT INTO WeatherConditions (temperature, humidity, is_raining) VALUES (?, ?, ?)',
                   (temperature, humidity, is_raining))

    # Случайные данные о влажности почвы
    moisture_level = round(random.uniform(5, 80), 1)  # Уровень влажности почвы от 5 до 80
    cursor.execute('INSERT INTO SoilMoisture (moisture_level) VALUES (?)', (moisture_level,))

    conn.commit()
    conn.close()

# Функция для фаззификации входных данных
def fuzzify(temperature, humidity, is_raining):
    if is_raining:
        return "high", "low"  # Возвращаем значения по умолчанию при дожде

    # Определяем уровень влажности
    if humidity < 40:
        humidity_level = "low"
    elif humidity < 70:
        humidity_level = "medium"
    else:
        humidity_level = "high"

    # Определяем уровень температуры
    if temperature < 20:
        temperature_level = "low"
    elif temperature < 30:
        temperature_level = "medium"
    else:
        temperature_level = "high"

    return humidity_level, temperature_level

# Функция для генерации случайного времени суток и его нечёткой категории
def generate_random_time_of_day():
    time_categories = ["утро", "день", "вечер", "ночь"]
    times = ["06:00:00", "12:00:00", "18:00:00", "00:00:00"]
    index = random.randint(0, 3)
    return times[index], time_categories[index]

# Функция для дефаззификации с учётом времени суток
def defuzzify(humidity_level, temperature_level, time_of_day_category):
    if time_of_day_category == "утро":
        if humidity_level == "low" and temperature_level == "high":
            return 6  # Много полива утром
        elif humidity_level == "medium" and temperature_level == "medium":
            return 4  # Средний полив утром
        elif humidity_level == "high" and temperature_level == "low":
            return 2  # Мало полива утром
    elif time_of_day_category == "день":
        if humidity_level == "low" and temperature_level == "high":
            return 5  # Много полива днём
        elif humidity_level == "medium" and temperature_level == "medium":
            return 3  # Средний полив днём
        elif humidity_level == "high" and temperature_level == "low":
            return 1  # Мало полива днём
    elif time_of_day_category == "вечер":
        if humidity_level == "low" and temperature_level == "high":
            return 4  # Много полива вечером
        elif humidity_level == "medium" and temperature_level == "medium":
            return 3  # Средний полив вечером
        elif humidity_level == "high" and temperature_level == "low":
            return 2  # Мало полива вечером
    else:  # ночь
        if humidity_level == "low" and temperature_level == "high":
            return 3  # Много полива ночью
        elif humidity_level == "medium" and temperature_level == "medium":
            return 2  # Средний полив ночью
        elif humidity_level == "high" and temperature_level == "low":
            return 1  # Мало полива ночью

    return 2  # Нормальное количество полива по умолчанию

# Симуляция процесса управления поливом
def simulate_irrigation(conn):
    cursor = conn.cursor()

    # Получаем последние данные о погоде и влажности почвы
    cursor.execute("SELECT * FROM WeatherConditions ORDER BY id DESC LIMIT 1")
    weather_conditions = cursor.fetchone()

    cursor.execute("SELECT * FROM SoilMoisture ORDER BY id DESC LIMIT 1")
    soil_moisture = cursor.fetchone()

    # Фаззификация входных данных
    humidity_level, temperature_level = fuzzify(weather_conditions[1], weather_conditions[2], weather_conditions[3])

    # Случайное время суток и его нечёткая категория
    random_time, time_of_day_category = generate_random_time_of_day()

    # Дефаззификация для получения количества полива с учётом времени суток
    irrigation_amount = defuzzify(humidity_level, temperature_level, time_of_day_category)

    # Вывод результата
    print("\nВремя:", random_time)
    print("Температура (°C):", weather_conditions[1])
    print("Влажность (%):", weather_conditions[2])
    print("Идёт дождь:", "Да" if weather_conditions[3] else "Нет")
    print("\nНечёткие данные:")
    print("- Время суток:", time_of_day_category)
    print("- Уровень влажности:", humidity_level)
    print("- Уровень температуры:", temperature_level)
    print(f"\nРекомендуемое количество полива: {irrigation_amount} литров.")

# Основная функция для запуска всех операций
def main():
    database = "irrigation_system.db"
    create_database(database)

    generate_random_data(database)

    connection = sqlite3.connect(database)
    simulate_irrigation(connection)
    connection.close()

if __name__ == '__main__':
    main()
