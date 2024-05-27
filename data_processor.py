import pandas as pd
import os
from utils import dict_to_ini, sanitize_string, read_series_tcc_ini, download_pdf, log_message
from concurrent.futures import ThreadPoolExecutor


# Объединяет xlsx файлы страниц скачанные с сайта в один большой CSV.
# Сортирует по серии, температурному режиму и ссылке на даташит.
def process_csv():
    # Путь к папке с файлами XLSX
    xlsx_folder = "output/temp_xlsx_pages/"

    # Список для хранения данных из всех файлов
    all_data = []

    # Чтение данных из каждого файла XLSX и добавление их в список
    for filename in os.listdir(xlsx_folder):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(xlsx_folder, filename)
            df = pd.read_excel(filepath)
            all_data.append(df)

    # Объединение данных из всех файлов в один DataFrame
    merged_df = pd.concat(all_data, ignore_index=True)

    # Сортировка данных по столбцу "Series"
    merged_df_sorted = merged_df.sort_values(by=['Series', 'TCC', 'Datasheet'])

    # Сохранение отсортированного DataFrame в файл CSV с точкой с запятой в качестве разделителя
    merged_csv_path = "output/yageo_mlcc.csv"
    merged_df_sorted.to_csv(merged_csv_path, index=False, sep=';')

    log_message(f"Объединенный и отсортированный файл сохранен в формате CSV: {merged_csv_path}")


# Подготавливает директории для даташитов (создает директории в формате series+tcc)
def series_dir_prep():
    # Чтение CSV файла
    df = pd.read_csv("output/!yageo_mlcc.csv", sep=';')

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
        directory_path = os.path.join("output", "datasheet", directory_name)
        os.makedirs(directory_path, exist_ok=True)

        # Создание INI файла c series и tcc
        ini_file = os.path.join(directory_path, "series_tcc.ini")
        dict_to_ini(series_tcc, ini_file)

        log_message(f'[+] Директория создана: {directory_path}')


def process_directory(directory):
    series_tcc = read_series_tcc_ini(directory)
    if series_tcc:
        csv_file = "output/yageo_mlcc.csv"
        df = pd.read_csv("output/!yageo_mlcc.csv", sep=';')
        df.columns = map(str.lower, df.columns)

        for column in ['series', 'tcc']:
            mask = df[column].str.contains(series_tcc[column], case=False, na=False)
            df = df[mask]

        # Копирование строк в новый CSV файл
        csv_filename = "yageo_mlcc_" + os.path.basename(directory) + '.csv'
        copied_csv = os.path.join(directory, csv_filename)
        df.to_csv(copied_csv, index=False, header=True, sep=';')

        for datasheet_url in df['datasheet']:
            if pd.notnull(datasheet_url) and datasheet_url.strip():  # Проверка наличия URL и его содержимого
                log_message("[!] Скачиваю datasheet")
                output_file = os.path.join(directory, os.path.basename(datasheet_url))
                download_pdf(datasheet_url, output_file)
            else:
                log_message(f"[!] Нет ссылки на datasheet в ячейке {datasheet_url}")

        directory = os.path.join(directory, "spec sheets")
        if not os.path.exists(directory):
            os.makedirs(directory)

        for specsheet_url in df['spec sheet link']:
            if pd.notnull(specsheet_url) and specsheet_url.strip():  # Проверка наличия URL и его содержимого
                log_message("[!] Скачиваю specsheet")
                output_file = os.path.join(directory, os.path.basename(specsheet_url)) + ".pdf"
                download_pdf(specsheet_url, output_file)
            else:
                log_message(f"[!] Нет ссылки на specsheet в ячейке {specsheet_url}")


def process_datasheet_directories():
    datasheet_directory = os.path.join("output", "datasheet")
    for subdir in os.listdir(datasheet_directory):
        subdirectory_path = os.path.join(datasheet_directory, subdir)
        log_message(subdirectory_path)
        if os.path.isdir(subdirectory_path):
            process_directory(subdirectory_path)
