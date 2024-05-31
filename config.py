LOG_DIRECTORY = 'logs/'
# категория элементов с сайта
ELEMENT_CATEGORY = 'mlcc'

# URL страницы с поиском элементов.
# Используется при скачивании списка всех элементов в рамках одной категории с помощью selenium
BASE_URL = 'https://www.yageo.com/en/ProductSearch'

# Путь к папке с файлами XLSX (экспорты страниц результатов поиска элементов)
XLSX_TEMP_PATH = "output/" + ELEMENT_CATEGORY + "/temp_xlsx_pages/"

# Файл для хранения DataFrame с данными из всех XLSX файлов в формате csv
MERGED_CSV_PATH = "output/rchip/yageo_" + ELEMENT_CATEGORY + ".csv"

# Директория в которой хранятся даташиты
DATASHEET_DIRECTORY = "output/" + ELEMENT_CATEGORY + "/datasheet/"

# путь хранения файла с индексами
INDEX_FILE_PATH = "output/" + ELEMENT_CATEGORY + "/index.json"
