import os
import pandas as pd
from utils.downloader import download_file
from utils.logger import log_message
from utils.text_operations import read_series_tcc_ini, sanitize_string, dict_to_ini


# Подготавливает директории для даташитов (создает директории в формате series+tcc)
def series_dir_prep(merged_csv_path):
    # Чтение CSV файла
    df = pd.read_csv(merged_csv_path, sep=';')

    # Уникальные пары значений Series и TCC
    unique_pairs = df[['Series', 'TCC']].drop_duplicates()

    # Создание директорий для каждой уникальной пары
    for _, row in unique_pairs.iterrows():
        series = row['Series']
        tcc = row['TCC']

        # записываем изначальные series и tcc
        log_message(f'series: "{series}", tcc "{tcc}"')
        series_tcc = {"Series": series, "TCC": tcc}

        # Проверка на наличие слеша в Series
        if '/' in series:
            series = series.split(' ')[0]  # Берем только символы до пробела
        series = sanitize_string(series)

        # Проверка на наличие TCC в Series
        if tcc.lower() in series.lower():
            directory_name = series
        else:
            directory_name = f"{series} {tcc}"

        # создаем новые директории
        directory_path = os.path.join("../output", "datasheet", directory_name)
        os.makedirs(directory_path, exist_ok=True)

        # Создание INI файла c series и tcc
        ini_file = os.path.join(directory_path, "series_tcc.ini")
        dict_to_ini(series_tcc, ini_file)

        log_message(f'[+] Директория создана: {directory_path}')


# TODO: убрать mlcc
# Копирование строк из основного в новый маленький CSV файл
def create_small_csv(directory, dataframe):
    csv_filename = "yageo_mlcc_" + os.path.basename(directory) + '.csv'
    copied_csv = os.path.join(directory, csv_filename)
    dataframe.to_csv(copied_csv, index=False, header=True, sep=';')


# Получает ссылку на скачивание pdf файла (specsheet или datasheet) из datafame
# df - объект dataframe
# column - строка, название столбца
# directory - стока, путь рабочей поддиректории
def get_download_url_from_dataframe(directory, df, column):
    filetype = 'datasheet'
    if column == 'spec sheet link':
        filetype = 'specsheet'
    for url in df[column]:
        if pd.notnull(url) and url.strip():  # Проверка наличия URL и его содержимого
            log_message(f"[!] Скачиваю {filetype}")
            output_file = os.path.join(directory, os.path.basename(url))
            if ".pdf" not in url:
                output_file += ".pdf"
            download_file(url, output_file)
        else:
            log_message(f"[-] Нет ссылки на {filetype} в ячейке {url}")


# метод, который смотрит датафрейм и понимает откуда скачивать и пихать даташиты
def process_directory(directory, merged_csv_path):
    # читаем ини, чтобы понять что за серия и tcc в этой папке
    series_tcc = read_series_tcc_ini(directory)
    if series_tcc:
        df = pd.read_csv(merged_csv_path, sep=';')
        df.columns = map(str.lower, df.columns)

        # вытаскиваем только те строки из csv, которые совпадают с серией и tcc из csv
        for column in ['series', 'tcc']:
            mask = df[column].str.contains(series_tcc[column], case=False, na=False)
            df = df[mask]

        # Создаем мелкий csv c используемыми компонентами в текущей серии
        create_small_csv(directory, df)

        # Ищем ссылки на скачивание даташитов в csv и скачиваем их
        get_download_url_from_dataframe(directory, df, 'datasheet')

        directory = os.path.join(directory, "spec sheets")
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Ищем ссылки на скачивание спекшитов в csv и скачиваем их
        get_download_url_from_dataframe(directory, df, 'spec sheet link')


# метод, который прогоняет по всем папкам и пихает в них даташиты
def process_datasheet_directories(merged_csv_path, datasheet_directory):
    # datasheet_directory = os.path.join("output", "datasheet")
    for subdir in os.listdir(datasheet_directory):
        subdirectory_path = os.path.join(datasheet_directory, subdir)
        log_message(subdirectory_path)
        if os.path.isdir(subdirectory_path):
            process_directory(subdirectory_path, merged_csv_path)

