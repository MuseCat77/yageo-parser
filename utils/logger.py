import logging
import os
from datetime import datetime
from config import LOG_DIRECTORY as log_directory

log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_filepath = os.path.join(log_directory, log_filename)

# Создание директории для логов
os.makedirs(log_directory, exist_ok=True)

# Настройка логирования
# Имя лог-файла на основе времени и даты запуска программы
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[
    logging.FileHandler(log_filepath, encoding='utf-8'),
    logging.StreamHandler()
])


# Вывод сообщения в консоль через логгер
def log_message(message):
    logging.info(message)
    # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(f"[{current_time}] {message}")
