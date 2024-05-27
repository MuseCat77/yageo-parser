import pandas as pd
import os
from utils.logger import log_message


# Объединяет xlsx файлы страниц скачанные с сайта в один большой CSV.
# Сортирует по серии, температурному режиму и ссылке на даташит.
def process_csv(xlsx_temp_path, merged_csv_path):
    # Список для хранения данных из всех файлов
    all_data = []

    # Чтение данных из каждого файла XLSX и добавление их в список
    for filename in os.listdir(xlsx_temp_path):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(xlsx_temp_path, filename)
            df = pd.read_excel(filepath)
            all_data.append(df)
            log_message(f"Обработан файл {filename}")

    # Объединение данных из всех файлов в один DataFrame
    merged_df = pd.concat(all_data, ignore_index=True)
    log_message("Импорт данных в датафрейм...")

    # Сортировка данных по столбцу "Series"
    merged_df_sorted = merged_df.sort_values(by=['Series', 'TCC', 'Datasheet'])
    log_message("Сортировка данных...")

    # Сохранение отсортированного DataFrame в файл CSV с точкой с запятой в качестве разделителя
    merged_df_sorted.to_csv(merged_csv_path, index=False, sep=';')
    log_message(f"Объединенный и отсортированный файл сохранен в формате CSV: {merged_csv_path}")
