from utils.logger import log_message
import os
import pandas as pd
import json


# Функция для обновления данных из missing_datasheet_elements.csv в соответствующие csv
def join_missing_datasheet(index_filepath, missing_data_csv):
    missing_data_csv += "missing_datasheet_elements.csv"
    log_message(missing_data_csv)
    # Загрузка JSON файла
    with open(index_filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    # Проход по каждому CSV файлу из JSON и обновление его данными из missing_datasheet_elements.csv
    for filename, details in data.items():
        filepath = os.path.join(details['base_dir'], filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath, sep=";")
            missing_data = pd.read_csv(missing_data_csv, sep=";")

            # Создаем пустой DataFrame для совпадающих данных
            matching_data = pd.DataFrame()

            # Проходим по каждому элементу списка tcc из details
            for tcc in details['tcc']:
                # Фильтруем данные из missing_data, где совпадают series и текущий элемент tcc
                matching_data_part = missing_data[
                    (missing_data['Series'] == details['series']) & (missing_data['TCC'] == tcc)]
                # Добавляем только совпадающие данные, которых нет в df по полю Part Number
                matching_data = pd.concat(
                    [matching_data, matching_data_part[~matching_data_part['Part Number'].isin(df['Part Number'])]],
                    ignore_index=True)

            # Добавление совпадающих строк в CSV файл
            if not matching_data.empty:
                for index, row in matching_data.iterrows():
                    log_message(f"Найдено совпадение в строке {index + 1}:")
                    log_message(f"Series: {row['Series']}, TCC: {row['TCC']}")
                df = pd.concat([df, matching_data], ignore_index=True)

            # Сохранение обновленного CSV файла
            df.to_csv(filepath, index=False, sep=";")
