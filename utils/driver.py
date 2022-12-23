from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# функция получения объекта веб-драйвера
def get_driver(path_to_driver: str) -> WebDriver:
    service = Service(executable_path=path_to_driver)
    return webdriver.Chrome(service=service)
