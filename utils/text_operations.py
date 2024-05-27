import re
import configparser
import os
from urllib.parse import urlparse


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


def extract_filename_from_url(url):
    # Парсинг URL для извлечения имени файла без расширения
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    file_without_extension = os.path.splitext(filename)[0]
    return file_without_extension


def extract_version(filename):
    # Извлечение версии из имени файла, если версия указана
    match = re.search(r'V_(\d+)$', filename)
    return int(match.group(1)) if match else None


def extract_base_datasheet_filename(filename):
    # Извлечение базового имени файла даташита без версии
    return re.sub(r'V_\d+$', '', filename)
