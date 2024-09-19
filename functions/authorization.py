import time
import logging
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot.config import Config
from db.commands import store_truck_info

logger = logging.getLogger(__name__)


def get_random_chrome_user_agent():
    try:
        user_agent = UserAgent(browsers='chrome', os='macos', platforms='pc')
        return user_agent.random
    except Exception as e:
        logger.error(f'Ошибка /get_random_chrome_user_agent: {e}.')


async def authorization(login: str, password: str):
    options = webdriver.ChromeOptions()
    options.add_argument(get_random_chrome_user_agent())
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(Config.AUTHORIZATION_URL)
        wait = WebDriverWait(driver, 5)

        # ввод логина
        login_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_login')))
        login_input = login_input_container.find_element(By.TAG_NAME, 'input')
        login_input.clear()
        login_input.send_keys(login)

        # ввод пароля
        pass_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_password')))
        pass_input = pass_input_container.find_element(By.TAG_NAME, 'input')
        pass_input.clear()
        pass_input.send_keys(password)

        # нажатие кнопки "войти"
        input_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_login')))
        input_button = input_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        input_button.click()
        time.sleep(3)

        # получаем данные о заявках с главной страницы и записываем их в БД
        soup = BS(driver.page_source, 'html.parser')
        time.sleep(4)
        if soup is not None:
            await store_truck_info(soup)    # заполняем таблицу
            return True
        else:
            return False

    except Exception as e:
        logger.error(f'Ошибка /authorization: {e}.')
        return False

    finally:
        driver.close()
        driver.quit()
