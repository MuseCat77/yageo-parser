import os
import shutil
import pandas as pd
import difflib


# Путь к CSV файлу
csv_file_path = '../output/mlcc/yageo_mlcc.csv'

# Директория с файлами парт намберов
source_directory = '../output/mlcc/datasheet/tmp'

# Основная директория для перемещения файлов
destination_base_directory = 'output/mlcc/datasheet'

# Чтение CSV файла
df = pd.read_csv(csv_file_path, sep=";")


# Получение списка всех доступных директорий в основной директории
available_directories = [
    name for name in os.listdir(destination_base_directory)
    if os.path.isdir(os.path.join(destination_base_directory, name))
]


# Функция для поиска наиболее похожей директории
def find_closest_directory(target, directories):
    closest_match = difflib.get_close_matches(target, directories, n=1, cutoff=0.1)
    return closest_match[0] if closest_match else None


# Обход каждой строки в DataFrame
for index, row in df.iterrows():
    part_number = row['Part Number']
    datasheet = row['Datasheet']

    # Пропустить строки с пустым или NaN значением в столбце 'Datasheet'
    if pd.isnull(datasheet) or not datasheet.strip():
        print(f'Skipping part number {part_number} due to empty or NaN Datasheet value')
        continue

    # Формирование пути к файлу с парт намбером
    source_file_path = os.path.join(source_directory, part_number + ".pdf")

    # Извлечение имени файла из ссылки Datasheet
    datasheet_filename = os.path.basename(datasheet)
    if '.pdf' in datasheet_filename:
        datasheet_filename = str(datasheet_filename)[0:-4]

    closest_directory = find_closest_directory(datasheet_filename, available_directories)
    if not closest_directory:
        print(f'No matching directory found for {datasheet_filename}, skipping part number {part_number}')
        continue

    # destination_directory = os.path.join(destination_base_directory, datasheet_filename, 'specsheets')
    destination_directory = os.path.join(destination_base_directory, closest_directory, 'specsheets')

    # Создание директории назначения, если она не существует
    os.makedirs(destination_directory, exist_ok=True)

    # Формирование пути для перемещения файла
    destination_file_path = os.path.join(destination_directory)

    # Перемещение файла
    if os.path.exists(source_file_path):
        shutil.move(source_file_path, destination_file_path)
        print(f'Moved {source_file_path} to {destination_file_path}')
    else:
        print(f'File {source_file_path} does not exist')

print('Done!')
