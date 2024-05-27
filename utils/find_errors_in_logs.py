import os
import re


def find_error_lines(directory):
    # Регулярное выражение для поиска подстроки "Ошибка"
    pattern = re.compile(r'Ошибка')
    # Кодировка для файлов в ANSI
    encoding = 'cp1251'

    # Проходим по всем файлам в указанной директории
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Открываем каждый файл и читаем его построчно
            try:
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    for line_number, line in enumerate(f, start=1):
                        if pattern.search(line):
                            print(f"Файл: {file_path}, Строка {line_number}: {line.strip()}")
            except Exception as e:
                print(f"Не удалось прочитать файл {file_path}: {e}")



find_error_lines('../logs')
