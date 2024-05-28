from parser.download_list import scrape_and_download_xlsx
from parser.csv_processor import process_csv
from parser.make_datasheet_dirs import make_datasheet_dirs
from parser.datasheet_downloader import download_sheets
from parser.join_missing_datasheet import join_missing_datasheet
from config import BASE_URL, ELEMENT_CATEGORY, XLSX_TEMP_PATH, MERGED_CSV_PATH, DATASHEET_DIRECTORY


def main():
    choice = input('''1) Скачивание таблиц (список всех элементов)
2) Сшить csv со всеми элементами
3) Подготовить директории для datasheet
4) Скачать datasheet файлы
5) Скачать specsheet файлы
6) Распределить недостающие элементы без datasheet по маленьким спискам
''')
    if choice == "1":
        scrape_and_download_xlsx(BASE_URL, ELEMENT_CATEGORY, XLSX_TEMP_PATH)
    elif choice == "2":
        process_csv(XLSX_TEMP_PATH, MERGED_CSV_PATH)
    elif choice == "3":
        make_datasheet_dirs(MERGED_CSV_PATH, DATASHEET_DIRECTORY)
    elif choice == "4":
        download_sheets(DATASHEET_DIRECTORY, 'datasheet')
    elif choice == "5":
        download_sheets(DATASHEET_DIRECTORY, 'specsheet')
    elif choice == "6":
        join_missing_datasheet(DATASHEET_DIRECTORY)


if __name__ == "__main__":
    main()
