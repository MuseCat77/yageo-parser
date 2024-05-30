## Структура директорий:
```
yageo-parser/
├── output/                                    # Результаты парсинга
│   ├── mlcc/                                  # Директория с даташитами конденсаторов
│   │   ├── datasheet/
|   |   |   ├──	UPY-4C-Array_16V-to-100V_5     # Папка конкретного даташита
|   |   |   ├──	UPY-AC-Array_NP0X7R_0
|   |   |   ├──	UPY-AC_HiCap_X7RX7S_1
|   |   |   |   ├── UPY-AC_HiCap_X7RX7S_1.pdf  # Даташит серии конденсаторов
|   |   |   |   ├── UPY-AC_HiCap_X7RX7S_1.csv  # Список конденсаторов серии и их характеристики
|   |   |   |   ...
|   |   |   └──	tmp/                           # Временное расположение спекшитов всех конденсаторов
│   │   ├── temp_xlsx_pages/                   # Экспортированные страницы со всеми конденсаторами с сайта
│   │   ├── index.json                         # Индексный файл с путями к даташиту серии и картинкам
│   │   └── yageo_mlcc.csv                     # Список всех конденсаторов с сайта и их характеристики
│   ├── rchip/                                 # Директория с даташитами резисторов
│   │   ├── datasheet/
│   │   ├── temp_xlsx_pages/
│   │   ├── index.json
│   │   └── yageo_rchip.csv
│   └── example.json                           # Пример индекесного файла
├── parser/                                    # Скрипты для парсинга
│   ├── __pycache__/
│   ├── csv_processor.py                       # Обработка csv файлов
│   ├── datasheet_downloader.py                # Поиск ссылок на скачивание даташитов и спекшитов с помощью запросов
│   ├── download_list.py                       # Скачивание списка всех элементов с сайта с помощью selenium webdriver в xlsx
│   ├── join_missing_datasheet.py              # Ищет потерявшиеся компоненты, у которых не оказалось ссылки на даташит в списке
│   ├── make_datasheet_dirs.py                 # Подготавливает директории для скачивания даташитов
│   └── __init__.py
├── utils/                                     # Вспомогательные утилиты
│   ├── __pycache__/
│   ├── downloader.py                          # Скачивание файлов
│   ├── find_errors_in_logs.py
│   ├── logger.py                              # Логгирование и консольный вывод через logging
│   ├── make_json_index.py                     # Создание индексного файла
│   ├── migrate_datasheets.py                  # Перенос даташитов со старой структуры папок на новую
│   ├── pdf_operations.py
│   ├── text_operations.py                     # Обрабокта строк
│   └── __init__.py
├── .gitignore                                 # Игнорируемые файлы
├── config.py                                  # Конфигурационные настройки
├── main.py                                    # Основной скрипт для запуска парсера
└── requirements.txt                           # Зависимости проекта
```


На сайте нет спекшитов для rchip категории  
Нет спекшита для компонента [CQ0201BRNPO9BNR20](https://www.yageo.com/en/Chart/Download/pdf/CQ0201BRNPO9BNR20) (404)  
csv файлы хранятся в UTF-8 кодировке со знаком переноса CRLF и ";" в качестве разделителя
