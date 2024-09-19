import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lang.texts import *
from bot.config import Config
from functions.authorization import get_random_chrome_user_agent

logger = logging.getLogger(__name__)


async def fill_the_form(login: str, password: str, truck: str, trailer: str, trans_type: str, trans_species: str, date: str):
    options = webdriver.ChromeOptions()
    options.add_argument(get_random_chrome_user_agent())
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(Config.AUTHORIZATION_URL)
        wait = WebDriverWait(driver, 5)

        # ввод логина
        login_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_login')))
        login_input = login_input_container.find_element(By.TAG_NAME, 'input')
        login_input.send_keys(login)

        # ввод пароля
        pass_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_password')))
        pass_input = pass_input_container.find_element(By.TAG_NAME, 'input')
        pass_input.send_keys(password)

        # нажатие кнопки "войти"
        input_button_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btn_login')))
        input_button = input_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        input_button.click()
        time.sleep(2)

        # нажатие кнопки "Создать заявку"
        form_button_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btn_create_request')))
        form_button = form_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_._3oLjlNg_')
        form_button.click()
        time.sleep(0.5)

        # выбор тягача
        auto_target_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'lyt_car')))
        auto_target_container.click()
        auto_target = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='_1ewnVtMF' and contains(text(), '{truck}')]")))
        auto_target.click()

        # выбор прицепа
        if trailer != '':
            auto_target_container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'lyt_step_trailer')))
            auto_target_container.click()
            auto_target = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='_1ewnVtMF' and contains(text(), '{trailer}')]")))
            auto_target.click()

        # нажатие кнопки "Дальше"
        next_button_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btn_step_next')))
        next_button = next_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        next_button.click()
        time.sleep(0.5)

        # выбор типа перевозки
        trans_type_target_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'lyt_transportation')))
        trans_type_target_container.click()
        trans_type_ = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='_1ewnVtMF' and contains(text(), '{trans_type}')]")))
        trans_type_.click()

        # выбор вида перевозки
        kind_type_target_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'lyt_kind')))
        kind_type_target_container.click()
        kind_type = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='_1ewnVtMF' and contains(text(), '{trans_species}')]")))
        kind_type.click()

        # нажатие кнопки "Скопировать данные из профиля"
        checkbox_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'chk_copy')))
        checkbox_input = checkbox_container.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox_input)

        # нажатие кнопки "Дальше"
        next_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_step_next')))
        next_button = next_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        next_button.click()
        time.sleep(0.25)

        # нажатие кнопки "Я не робот"
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@data-testid="checkbox-iframe"]')))
        driver.switch_to.frame(iframe)
        captcha_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'js-button')))
        if captcha_container.is_displayed() and captcha_container.is_enabled():
            driver.execute_script("arguments[0].scrollIntoView(true);", captcha_container)
            captcha_container.click()
        driver.switch_to.default_content()
        time.sleep(1)

        # открытие селектора для выбора даты
        data_container = wait.until(EC.presence_of_element_located((By.ID, 'tab_steps')))
        data_selector = data_container.find_element(By.ID, 'dtx_date')
        data_selector.click()

        # заполнения поля "Input date" датой "текущая + 2 недели"
        data_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="_2pDYp-fi"]/input[@class="_1lKqd6Xg"]')))
        data_input.send_keys(date)

        # нажатие кнопки "Сохранить"
        save_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_3J1cw2n9')))
        save_button.click()
        time.sleep(0.25)

        # кнопка "Создать"
        create_request_container = wait.until(EC.presence_of_element_located((By.ID, 'lyt_btns')))
        create_request_button = create_request_container.find_element(By.ID, 'btn_step_next')
        create_request = create_request_button.find_element(By.CLASS_NAME, '_1YUb7Yf_')

        # выбор временного слота и отправка заявки
        time_container = wait.until(EC.presence_of_element_located((By.ID, 'lyt_slots')))
        for i in range(0, 24):
            time_selector = time_container.find_element(By.ID, f'lyt_slot_clone_{str(i)}')
            time_temp = time_selector.find_element(
                By.XPATH, ".//div[@class='_1SfRmVRt lbl_lbl51691592376684  label semibold _2ntznnGK semibold']").text
            try:
                time_selector.click()
                if create_request.is_enabled():
                    create_request.click()
                    return [SUCCESSFUL_FORM.format(truck, trailer if trailer else "отсутствует", trans_type,
                                                      trans_species, date, time_temp,
                                                      datetime.now().strftime("%H:%M:%S")), True]
            except Exception as e:
                print(f'Ошибка /time_selector: {e}')
                return [ERROR_FORM, False]

        return [ERROR_NO_TIME_FORM.format(datetime.now().strftime("%H:%M:%S")), False]

    except Exception as e:
        error_message = str(e).splitlines()[0]
        logger.error(f'Ошибка /fill_the_form: {error_message}')
        return [ERROR_FORM, False]

    finally:
        time.sleep(0.5)
        driver.close()
        driver.quit()
