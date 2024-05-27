from yageo_table_downloader import scrape_and_download_xlsx
from data_processor import process_csv, series_dir_prep, process_datasheet_directories

def main():
    category = 'mlcc'
    choice = input('''1) Скачивание таблиц (список всех элементов)
2) Сшить csv со всеми элементами
3) Подготовить директории для datasheet
4) Скачать datasheet / specsheet файлы
''')
    if choice == "1":
        scrape_and_download_xlsx(category)
    elif choice == "2":
        process_csv()
    elif choice == "3":
        series_dir_prep()
    elif choice == "4":
        process_datasheet_directories()


if __name__ == "__main__":
    main()
