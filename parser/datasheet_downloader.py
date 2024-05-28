import os
import pandas as pd
from utils.downloader import download_file
from utils.logger import log_message


def get_download_url_from_dataframe(directory, df, filetype):
    column = 'Datasheet'
    if filetype == 'specsheet':
        column = 'spec sheet link'
    for url in df[column]:
        if pd.notnull(url) and url.strip():  # Проверка наличия URL и его содержимого
            log_message(f"[!] Скачиваю {filetype}")
            output_file = os.path.join(directory, os.path.basename(url))
            if ".pdf" not in url:
                output_file += ".pdf"
            download_file(url, output_file)
        else:
            log_message(f"[-] Нет ссылки на {filetype} в ячейке {url}")


def download_sheets(base_dir, filetype):
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

            for csv_file in csv_files:
                csv_path = os.path.join(directory_path, csv_file)
                df = pd.read_csv(csv_path, sep=';')

                # Вызов вашей функции для обработки DataFrame
                if filetype == "datasheet":
                    get_download_url_from_dataframe(directory_path, df, 'datasheet')
                elif filetype == "specsheet":
                    directory_path = os.path.join(directory_path, "specsheets")
                    os.makedirs(directory_path, exist_ok=True)
                    get_download_url_from_dataframe(directory_path, df, 'specsheet')
