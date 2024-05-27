import os
import pandas as pd
from utils.text_operations import extract_filename_from_url, extract_version, extract_base_datasheet_filename
from utils.logger import log_message
from parser.csv_processor import create_small_csv


def read_datasheet_urls_and_find_missing(csv_file):
    # Чтение CSV файла и извлечение значений столбца Datasheet
    df = pd.read_csv(csv_file, sep=';')
    datasheet_urls = df['Datasheet']

    # Уникальные URL и строки с пропущенными значениями
    unique_urls = datasheet_urls.dropna().unique()
    missing_datasheet_rows = df[datasheet_urls.isna()]

    return unique_urls, missing_datasheet_rows


# Создание директорий для каждого даташита
def create_directories_for_datasheets(datasheet_filenames, base_directory):
    # Создание директорий для каждого имени файла с учетом версий
    os.makedirs(base_directory, exist_ok=True)
    latest_versions = {}

    for filename in datasheet_filenames:
        version = extract_version(filename)
        base_filename = extract_base_datasheet_filename(filename)

        # Проверка наличия более новой версии
        if base_filename not in latest_versions or (version and version > latest_versions[base_filename]['version']):
            if base_filename in latest_versions and os.path.exists(latest_versions[base_filename]['path']):
                os.rmdir(latest_versions[base_filename]['path'])

            directory_path = os.path.join(base_directory, filename)
            os.makedirs(directory_path, exist_ok=True)
            latest_versions[base_filename] = {'version': version, 'path': directory_path}
            log_message(f"[+] Директория под Datasheet создана: {directory_path}")


# Сохранение строк с элементами для которых нет ссылки на даташит
# (обычно подойдет даташит элемента той же серии)
def save_missing_datasheet_elements_list(missing_df, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    output_file += 'missing_datasheet_elements.csv'
    missing_df.to_csv(output_file, index=False)
    log_message(f"[+] Список элементов без ссылки на Datasheet создан: {output_file}")


def make_datasheet_dirs(csv_file, datasheet_directory):
    # Чтение уникальных URL и строки с пропущенными значениями
    unique_urls, missing_datasheet_rows = read_datasheet_urls_and_find_missing(csv_file)

    # Извлечение имен файлов из URL
    filenames = [extract_filename_from_url(url) for url in unique_urls]

    # Создание директорий для каждого имени файла
    create_directories_for_datasheets(filenames, datasheet_directory)

    # Создание маленького csv с элементами которые имеют совпадающий даташит
    create_small_csv(csv_file, datasheet_directory)

    # Сохранение строк с пустыми ячейками в отдельный файл
    save_missing_datasheet_elements_list(missing_datasheet_rows, datasheet_directory)
