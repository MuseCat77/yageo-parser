import os
import requests
from utils.logger import log_message


def download_file(url, output_file):
    temp_output_file = output_file + ".tmp"
    try:
        if not os.path.exists(output_file):
            log_message(f"связь с космосом {url}")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(temp_output_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                os.rename(temp_output_file, output_file)
                log_message(f"[+] Файл скачан: {output_file}")
            else:
                log_message(f"[-] Ошибка при скачивании файла {url}")
        else:
            log_message(f"[ ] Файл уже существует: {output_file}")
    finally:
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)
