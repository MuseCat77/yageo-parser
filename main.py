from parser.download_list import scrape_and_download_xlsx
from parser.csv_processor import process_csv
from parser.dataspecsheet_processor import process_datasheet_directories, series_dir_prep
from config import BASE_URL, ELEMENT_CATEGORY, XLSX_TEMP_PATH, MERGED_CSV_PATH, DATASHEET_DIRECTORY


def main():
    choice = input('''1) Скачивание таблиц (список всех элементов)
2) Сшить csv со всеми элементами
3) Подготовить директории для datasheet
4) Скачать datasheet / specsheet файлы
''')
    if choice == "1":
        scrape_and_download_xlsx(BASE_URL, ELEMENT_CATEGORY, XLSX_TEMP_PATH)
    elif choice == "2":
        process_csv(XLSX_TEMP_PATH, MERGED_CSV_PATH)
    elif choice == "3":
        series_dir_prep(MERGED_CSV_PATH)
    elif choice == "4":
        process_datasheet_directories(MERGED_CSV_PATH, DATASHEET_DIRECTORY)


if __name__ == "__main__":
    main()
