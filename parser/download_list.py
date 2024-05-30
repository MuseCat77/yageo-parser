from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils.logger import log_message
import time
import os


def get_chromium_driver(download_dir):
    options = Options()
    # путь к исполняемому файлу Chromium
    options.binary_location = 'D:/SOFT/chrome-win/chrome.exe'

    # Настройки профиля браузера
    prefs = {
        "download.default_directory": download_dir,  # Указываем папку для загрузок
        "download.prompt_for_download": False,  # Отключаем запрос на место сохранения файлов
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Включаем безопасный поиск
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver


def scrape_and_download_xlsx(base_url, category, xlsx_download_path):
    download_dir = os.path.abspath(xlsx_download_path)
    os.makedirs(download_dir, exist_ok=True)
    driver = get_chromium_driver(download_dir)

    # Функция скачивает файл, в котором экспортирована текущая страница с элементами
    def download_xlsx():
        # тык на кнопку экспорта страницы
        download_button = driver.find_element(By.XPATH, '//*[@id="download_btn"]')
        download_button.click()

        # Ожидание скачивания файла в 1 сек
        time.sleep(0.5)

        # Номер текущей страницы для имени файла
        page_number = url.split("page=")[-1]

        # Имя только что скачанного файла
        filename = "ProductSearchDownload.xlsx"

        # Новое имя файла
        new_filename = f"yageo_{category}_page_{page_number}.xlsx"

        # переименовываем скачанный файл чтобы не было одинаковых имен
        while not os.path.exists(os.path.join(download_dir, filename)):
            time.sleep(0.1)
        if os.path.isfile(os.path.join(download_dir, filename)):
            os.rename(os.path.join(download_dir, filename), os.path.join(download_dir, new_filename))

        log_message(f"Скачана страница {page_number} из {total_pages}")

    try:
        url = f"{base_url}?category={category}&apply_filter=1&page_size=100&page=1"
        driver.get(url)

        # Получаем общее количество страниц
        try:
            total_pages_element = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[8]/div[2]')
            total_pages = int(total_pages_element.text.split()[-1])
        except IndexError:
            total_pages = 123

        # Скачиваем первую страницу
        download_xlsx()

        # Скачиваем остальные уже после того как получили количество страниц
        for page in range(2, total_pages + 1):
            url = f"{base_url}?category={category}&apply_filter=1&page_size=100&page={page}"
            driver.get(url)
            download_xlsx()
    finally:
        # Закрываем браузер когда все скачалось
        driver.quit()
