from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from config import USER_AGENT, DRIVER_PATH
from logger import logger


def _create_driver():
    """
        создаем вебдрайвер
    """
    options = Options()
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH,
                                  options=options)
        logger.debug("Драйвер создан успешно")

        return driver
    except WebDriverException as error:
        logger.warning(error.msg)


def _collect_posts_data(driver, request_link):
    """
        собираем данные постов
    """
    try:
        driver.get(request_link)
        posts_data = []
        all_posts = driver.find_elements(by=By.CLASS_NAME,
                                         value='iva-item-body-KLUuy')
        for post in all_posts:
            try:
                post_name = post.find_element(by=By.TAG_NAME, value='h3').text
            except BaseException:
                post_name = ' '
            try:
                post_price = post.find_element(
                    by=By.CLASS_NAME, value='iva-item-priceStep-uq2CQ').text
            except BaseException:
                post_price = ' '
            try:
                post_badge = post.find_element(
                    by=By.CLASS_NAME, value='iva-item-badgeBarStep-DJwW2').text
            except BaseException:
                post_badge = ' '
            try:
                post_params = post.find_element(
                    by=By.CLASS_NAME, value='iva-item-autoParamsStep-WzfS8').text
            except BaseException:
                post_params = ' '
            try:
                post_description = post.find_element(
                    by=By.CLASS_NAME, value='iva-item-descriptionStep-C0ty1').text
            except BaseException:
                post_description = ' '
            try:
                post_geo = post.find_element(
                    by=By.CLASS_NAME, value='iva-item-geo-_Owyg').text
            except BaseException:
                post_geo = ' '
            try:
                post_link = post.find_element(
                    by=By.TAG_NAME, value='a').get_attribute('href')
            except BaseException:
                post_link = ' '

            posts_data.append({'post_name': post_name,
                               'post_price': post_price,
                               'post_budge': post_badge,
                               'post_params': post_params,
                               'post_description': post_description,
                               'post_geo': post_geo,
                               'post_link': post_link,
                               })

        return posts_data
    except WebDriverException as error:
        logger.warning(error.msg)


def _close_driver(driver):
    """
        закрываем драйвер
    """
    try:
        driver.close()
        driver.quit()
        logger.debug('Драйвер успешно закрыт')
    except WebDriverException as error:
        logger.warning(error.msg)


def get_posts_data(request_link):
    driver = _create_driver()
    posts_data = _collect_posts_data(driver, request_link)
    _close_driver(driver)

    return posts_data
