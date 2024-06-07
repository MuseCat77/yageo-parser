import logging
import os
import pandas as pd
import json
from utils.logger import log_message
from loguru import logger


# Функция для получения всех уникальных значений из столбца, игнорируя регистр
def get_unique_tcc_values(filepath):
    df = pd.read_csv(filepath, sep=";")
    series_value = df['Series'].iloc[0] if 'Series' in df.columns else ''
    unique_tcc = df['TCC'].dropna().unique().tolist() if 'TCC' in df.columns else []
    return series_value, unique_tcc


@logger.catch
def make_json_index(base_dir, index_file_path):
    output_data = {}

    # Проход по поддиректориям первого уровня в base_dir
    for subdir in next(os.walk(base_dir))[1]:
        logger.debug(subdir)
        subdir_path = os.path.join(base_dir, subdir)
        for filename in os.listdir(subdir_path):
            if filename.endswith('.csv'):
                csv_filepath = os.path.join(subdir_path, filename)
                series, unique_tcc = get_unique_tcc_values(csv_filepath)
                logger.debug(filename)
                specsheets_dir = os.path.join(subdir_path, "specsheets")
                for specsheet in os.listdir(specsheets_dir):
                    logger.debug(specsheet)
                    # базовая директория "output/datasheet/UPY-AC-Array_NP0X7R_0/"
                    base = subdir_path.replace("\\", "/").replace("../", "") + '/'

                    # datasheet "output/datasheet/UPY-AC_HiCap_X7RX7S_1/UPY-AC_HiCap_X7RX7S_1.pdf"
                    pdf_datasheet = os.path.join(subdir_path, filename.replace('.csv', '.pdf')).replace("\\", "/").replace("../", "")

                    # speecsheet "output/datasheet/UPY-AC_HiCap_X7RX7S_1/specsheets/AC0603JRX8G9BN102.pdf"
                    pdf_speecsheet = os.path.join(subdir_path, "specsheets", specsheet).replace("\\", "/").replace("../", "")

                    # картинка элемента "output/datasheet/UPY-AC_HiCap_X7RX7S_1/images/AC0603JRX8G9BN102_0_1.png"
                    image = os.path.join(subdir_path, "images", specsheet.replace('.pdf', '_0_1.png')).replace("\\", "/").replace("../", "")
                    # Формирование структуры JSON для текущего файла
                    file_key = filename

                    if file_key not in output_data:
                        output_data[file_key] = []

                    output_data[file_key].append({
                        "base_dir": base,
                        "pdf": pdf_speecsheet,
                        "datasheet": pdf_datasheet,
                        "img": image,
                        "series": series,
                        "tcc": unique_tcc
                    })

    # Запись данных в output/index.json
    with open(index_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, ensure_ascii=False, indent=4)

    logger.success(f"Данные успешно сохранены в {index_file_path}")
