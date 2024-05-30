import os
import pandas as pd
import json
from utils.logger import log_message


# Функция для получения всех уникальных значений из столбца, игнорируя регистр
def get_unique_tcc_values(filepath):
    df = pd.read_csv(filepath, sep=";")
    series_value = df['Series'].iloc[0] if 'Series' in df.columns else ''
    unique_tcc = df['TCC'].dropna().unique().tolist() if 'TCC' in df.columns else []
    return series_value, unique_tcc


def make_json_index(base_dir, index_file_path):
    output_data = {}

    # Проход по поддиректориям первого уровня в base_dir
    for subdir in next(os.walk(base_dir))[1]:
        subdir_path = os.path.join(base_dir, subdir)
        for filename in os.listdir(subdir_path):
            if filename.endswith('.csv'):
                csv_filepath = os.path.join(subdir_path, filename)
                series, unique_tcc = get_unique_tcc_values(csv_filepath)

                # Формирование структуры JSON для текущего файла
                file_key = filename
                output_data[file_key] = {
                    "base_dir": subdir_path.replace("\\", "/").replace("../", "") + '/',
                    "pdf": os.path.join(subdir_path, filename.replace('.csv', '.pdf')).replace("\\", "/").replace("../",
                                                                                                                  ""),
                    "img": "",
                    "series": series,
                    "tcc": unique_tcc
                }

    # Запись данных в output/index.json
    with open(index_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, ensure_ascii=False, indent=4)

    log_message(f"Данные успешно сохранены в {index_file_path}")
