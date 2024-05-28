import os
import shutil


def copy_pdf_files(source_base_dir, destination_dir):
    # Проходимся по поддиректориям внутри source_base_dir
    for root, dirs, files in os.walk(source_base_dir):

        for file in files:
            if file.endswith('.pdf'):
                # Путь к исходному файлу
                source_file = os.path.join(root, file)
                # Путь к целевому файлу
                destination_file = os.path.join(destination_dir, file)
                # Копируем PDF файл
                shutil.copy2(source_file, destination_file)
                print(f'Copied: {source_file} to {destination_file}')


def main():
    source_base_dir = '../output.old/datasheet'
    destination_dir = '../output/datasheet/tmp'

    # Создаем целевую директорию, если она не существует
    os.makedirs(destination_dir, exist_ok=True)

    copy_pdf_files(source_base_dir, destination_dir)


if __name__ == "__main__":
    main()
