import re
import configparser
import os


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
