from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options
import time
import os

BASE_URL = 'https://www.yageo.com/en/ProductSearch'
DOWNLOAD_PATH = 'output/temp_xlsx_pages/'


# не скачивает автоматически и медленно стартует
def get_waterfox_driver(download_dir):
    options = Options()
    # путь к Waterfox
    options.binary_location = 'C:\Program Files\Waterfox\waterfox.exe'

    # Создание профиля браузера
    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)  # Используем указанную папку для загрузок
    profile.set_preference("browser.download.dir", download_dir)  # Указываем папку для загрузок
    profile.set_preference("browser.download.manager.showWhenStarting", False)  # Не показывать окно загрузок при старте
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/octet-stream")  # Не спрашивать, куда сохранять все типы файлов

    # Объединение профиля с опциями
    options.profile = profile

    driver = webdriver.Firefox(options=options)
    return driver


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


def scrape_and_download_xlsx(category):
    download_dir = os.path.abspath(DOWNLOAD_PATH)
    os.makedirs(download_dir, exist_ok=True)
    driver = get_chromium_driver(download_dir)

    def download_xlsx():
        download_button = driver.find_element(By.XPATH, '//*[@id="download_btn"]')
        download_button.click()
        page_number = url.split("page=")[-1]
        filename = "ProductSearchDownload.xlsx"
        new_filename = f"yageo_{category}_page_{page_number}.xlsx"
        # Ожидание скачивания файла
        time.sleep(1)
        os.rename(os.path.join(download_dir, filename), os.path.join(download_dir, new_filename))
        print(f"Скачана страница {page_number} из {total_pages}")

    try:
        url = f"{BASE_URL}?category={category}&apply_filter=1&page_size=100&page=1"
        driver.get(url)

        # Получаем общее количество страниц
        try:
            total_pages_element = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[8]/div[2]')
            total_pages = int(total_pages_element.text.split()[-1])
        except IndexError:
            total_pages = 123

        download_xlsx()

        for page in range(2, total_pages + 1):
            url = f"{BASE_URL}?category={category}&apply_filter=1&page_size=100&page={page}"
            driver.get(url)
            download_xlsx()
    finally:
        driver.quit()
