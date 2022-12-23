from selenium.webdriver.common.by import By

from utils.work_with_csv import CsvWriter
from utils.driver import get_driver

from one_teacher_parsing import teacher_parsing


# создаем функцию для парсинга
def parse_all_teachers(filename: str):
    """
    :param filename: название файла csv с результатом парсинга
    :return: None
    """

    # записываем данные о преподавателях с помощью функции CsvWriter
    csv_file = CsvWriter(filename)

    # создаем пустой список для ссылок на страницы преподавателей
    teacher_links = []

    # подключаемся к драйверу Хрома
    driver = get_driver("drivers/chromedriver")

    # заходим на главную страницу

    driver.get("https://wiki.mipt.tech")

    # задаем переменную, которая будет хранить xpath кафедр

    xpath = "//a[contains(@title, 'Кафедра') or " \
            "    contains(@title, 'Высшая школа системного') or " \
            "    contains(@title, 'Военная')] "

    # Забираем список объектов, соответсвующим тегам по тайтлам
    department_elements = driver.find_elements(By.XPATH, xpath)

    # создаём список ссылок для каждой каждой кафедры кроме кафедры биофизики и информатики (пустая тсраница)
    departments = [el.get_attribute("href") for el in department_elements
                   if "биофизики и экологии" not in el.get_attribute("title")]

    # Проходим по каждой ссылке на кафедру
    for department in departments:
        driver.get(department)

        # Пишем xpath до div элемента, содержащего список преподавателей под заголовком "Преподаватели кафедры"
        current_teachers_div_xpath = "//span[text()='Преподаватели кафедры']/parent::h2/following-sibling::div"
        # Переходим по xpath
        current_teachers_div = driver.find_element(By.XPATH, current_teachers_div_xpath)
        # Пытаемся получить атрибут class элемента, содержащего список преподавателей. Если атрибута нет,
        # то get_attribute возвращает None
        class_attribute = current_teachers_div.get_attribute("class")

        # Если аттрибут есть, то это список с фотографиями
        if class_attribute:
            teacher_elements = current_teachers_div.find_elements(By.XPATH, "//div[contains(@class, 'gallerytext')]/p/a")
        # Если атрбута нет, то это список без фото. К нему нужен другой Xpath
        else:
            teacher_elements = current_teachers_div.find_elements(By.TAG_NAME, "a")
        # В списке объектов с тегами "а" забираем значение атрибута href (ссылку на страницу преподавателя)
        for teacher_element in teacher_elements:
            teacher_links.append(teacher_element.get_attribute("href"))

    # Парсим страницы каждого преподавателя с помощью функции teacher_parsing
    for teacher_link in teacher_links:

        teacher = teacher_parsing(teacher_link, driver)

        csv_file.append_to_csv(teacher)
        csv_file.flush()

    driver.quit()


if __name__ == "__main__":
    # TODO генерировать имя по дате
    parse_all_teachers("csv/parsed.csv")
