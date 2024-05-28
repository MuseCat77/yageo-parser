import os
import re


def extract_base_name(name):
    """ Извлекает базовое имя файла или директории без версии """
    return re.sub(r'V_\d+', '', name).strip()


def copy_pdf_files(src_base_dir, dest_base_dir):
    # Создаем целевую директорию, если она не существует
    os.makedirs(dest_base_dir, exist_ok=True)

    # Проходим по всем поддиректориям в исходной базе
    for root, dirs, files in os.walk(src_base_dir):
        for file in files:
            if file.endswith('.pdf'):
                # Извлечение базового имени файла без версии
                base_filename = extract_base_name(file)

                # Путь к исходному файлу
                src_file_path = os.path.join(root, file)

                # Путь к целевой директории
                matching_dir = None
                for dir_name in os.listdir(dest_base_dir):
                    if extract_base_name(dir_name) == base_filename:
                        matching_dir = dir_name
                        break

                if matching_dir:
                    dest_dir_path = os.path.join(dest_base_dir, matching_dir)
                else:
                    dest_dir_path = dest_base_dir

                # Путь к целевому файлу
                dest_file_path = os.path.join(dest_dir_path, file)

                # Копируем файл в целевую директорию
                os.makedirs(dest_dir_path, exist_ok=True)
                with open(src_file_path, 'rb') as src_file:
                    with open(dest_file_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())

                print(f"Copied {src_file_path} to {dest_file_path}")


def main():
    src_base_dir = "../output.old/datasheet"
    dest_base_dir = "../output/datasheet"

    copy_pdf_files(src_base_dir, dest_base_dir)


if __name__ == "__main__":
    main()
