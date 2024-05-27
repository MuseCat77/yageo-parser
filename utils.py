import re
import configparser
import os
import requests
from datetime import datetime
import logging


# Создание директории для логов
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

# Имя лог-файла на основе времени и даты запуска программы
log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_filepath = os.path.join(log_directory, log_filename)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[
    logging.FileHandler(log_filepath),
    logging.StreamHandler()
])


def log_message(message):
    logging.info(message)
    # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(f"[{current_time}] {message}")


# Удаляем пробелы и экранируем специальные символы
def sanitize_string(s):
    return re.sub(r'[^\w\s]', '_', s)


# Сохранение словаря в ini например для хранения данных об изначальных данных в ячейках series и tcc
def dict_to_ini(dictionary, filename):
    config = configparser.ConfigParser()
    config.read_dict({'DEFAULT': dictionary})

    with open(filename, 'w') as configfile:
        config.write(configfile)


# Распаковка ini в словарь
def read_series_tcc_ini(directory):
    ini_file = os.path.join(directory, "series_tcc.ini")
    if os.path.exists(ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return dict(config['DEFAULT'])
    else:
        return None


def download_pdf(url, output_file):
    temp_output_file = output_file + ".tmp"
    try:
        if not os.path.exists(output_file):
            log_message(f"связь с космосом {url}")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(temp_output_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                os.rename(temp_output_file, output_file)
                log_message(f"[+] Файл скачан: {output_file}")
            else:
                log_message(f"[!] Ошибка при скачивании файла {url}")
        else:
            log_message(f"[ ] PDF файл уже существует: {output_file}")
    finally:
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)


# def ini_to_dict(filename):
#     config = configparser.ConfigParser()
#     config.read(filename)
#     dictionary = {}
#     for section in config.sections():
#         for key, value in config.items(section):
#             dictionary[key] = value
#     return dictionary
