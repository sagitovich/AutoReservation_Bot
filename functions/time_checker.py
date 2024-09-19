import json
import asyncio
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

from bot.config import Config
from functions.form_completion import fill_the_form
from db.commands import get_dates_to_check, take_info_via_date

logger = logging.getLogger(__name__)


async def check_dates():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    dates = await get_dates_to_check()
    try:
        for date in dates:
            driver.get(Config.CHECK_DATES_JSON.format(date))

            json_text = driver.find_element(By.TAG_NAME, 'pre').text
            data = json.loads(json_text)

            for item in data:
                try:
                    if item.get('free'):
                        form_info = await take_info_via_date(date=date)
                        info = await fill_the_form(login=Config.LOGIN, password=Config.PASSWORD,
                                                    truck=form_info[0], trailer=form_info[1],
                                                    trans_type=form_info[2], trans_species=form_info[3],
                                                    date=form_info[4])
                        print(info)

                except Exception as e:
                    print(f'Ошибка поиска времени: {e}')
                    pass

            info = (f'Мест не найдено\n'
                    f'Дата: {date[6:8]}.{date[4:6]}.{date[0:4]}\n'
                    f'Время проверки: {datetime.datetime.now()}\n\n')
            logger.info(info)

    except Exception as e:
        print(f'Error in /check_dates: {e}')
        pass


async def periodic_check_dates():
    while True:
        await asyncio.sleep(5)
        await check_dates()  # в среднем - секунда на выполнение
