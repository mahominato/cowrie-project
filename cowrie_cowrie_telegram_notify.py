import os
import time
import requests

# Токен и chat ID
BOT_TOKEN = "7688581546:AAEFMoj9WQVhLvrSWPToDEVirgcEBK-X2Cw"
CHAT_ID = "2111795303"

# Путь к логам Cowrie
LOG_PATH = "/home/neo/cowrie/var/log/cowrie/cowrie.log"

# Функция для отправки сообщений
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(f"Telegram response: {response.text}")

# Функция для мониторинга логов Cowrie
def monitor_cowrie_logs():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            f.seek(0, os.SEEK_END)  # Начинаем с конца файла
            while True:
                line = f.readline()
                if line:
                    if "New connection" in line:
                        send_telegram_message(f"Новое подключение в Cowrie: {line.strip()}")
                time.sleep(1)

# Функция для мониторинга подключений к порту 2222
def monitor_port_connections():
    previous_connections = set()

    while True:
        # Проверяем активные подключения к порту 2222 с помощью netstat
        result = os.popen("netstat -tn | grep ':2222'").read()
        current_connections = set(result.splitlines())

        # Выявляем новые подключения
        new_connections = current_connections - previous_connections

        if new_connections:
            for connection in new_connections:
                send_telegram_message(f"Новое подключение к порту 2222: {connection.strip()}")

        previous_connections = current_connections
        time.sleep(5)

# Запуск мониторинга
send_telegram_message("Мониторинг запущен!")

# Запуск двух мониторингов одновременно
try:
    monitor_cowrie_logs()
except:
    send_telegram_message("Ошибка при мониторинге логов Cowrie.")

monitor_port_connections()

