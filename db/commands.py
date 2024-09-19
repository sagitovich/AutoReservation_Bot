import logging

from db.schema import *
from lang.texts import *
from bot.config import Config

logger = logging.getLogger(__name__)


async def count_of_forms():
    try:
        return await Forms.query.where(Forms.form_id == Forms.form_id).gino.scalar()
    except Exception as e:
        logger.error(f'Ошибка /count_of_forms: {e}')
        return 0


async def list_of_forms():
    try:
        forms = await Forms.query.gino.all()
        forms_tuple = [(form.form_id, form.truck, form.trailer, form.trans_type,
                        form.trans_species, form.special_cargo, form.date) for form in forms]
        return forms_tuple
    except Exception as e:
        logger.error(f'Ошибка /create_novell_structure_for_novells: {e}')
        return []


async def take_form(form_id: int):
    try:
        form = await Forms.query.where(Forms.form_id == form_id).gino.first()
        form_list = [form.form_id, form.truck, form.trailer, form.trans_type,
                        form.trans_species, form.special_cargo, form.date]
        return form_list
    except Exception as e:
        logger.error(f'Ошибка /show_form: {e}')
        return []


async def add_form(truck: str, trailer: str, trans_type: str, trans_species: str, special_cargo: str, date: str):
    try:
        form_id = await count_of_forms()
        form = Forms(form_id=form_id+1, truck=truck, trailer=(trailer if trailer else ''), trans_type=trans_type,
                     trans_species=trans_species, special_cargo=(special_cargo if special_cargo else ''), date=date)
        await form.create()
    except Exception as e:
        logger.error(f'Ошибка /add_user: {e}')


async def rewrite_date(form_id: int, date: str):
    try:
        form = await Forms.query.where(Forms.form_id == form_id).gino.first()
        await form.update(date=date).apply()
    except Exception as e:
        logger.error(f'Ошибка /rewrite_date: {e}')


async def delete_form(form_id: int):
    try:
        form = await Forms.query.where(Forms.form_id == form_id).gino.first()
        await form.delete()
    except Exception as e:
        logger.error(f'Ошибка /delete_form: {e}')


async def store_truck_info(soup):
    try:
        divs = soup.find_all('div', class_='_4MZlMfg8')

        plates = []
        dates = []
        statuses = []

        for div in divs:
            text = div.get_text(strip=True)
            statuses_var = STATUSES
            if text in statuses_var:    # статус
                statuses.append(text)
            elif ":" in text:           # дата время
                dates.append(text)
            elif Config.PLATE_PATTERN.match(text):  # номер авто
                plates.append(text)

        for i in range(len(plates)):
            plate_upper = plates[i].upper()
            # Проверка, существует ли запись с таким номером тягача
            existing_truck = await Trucks.query.where(Trucks.truck == plate_upper).gino.first()

            if existing_truck:
                # Обновляем существующую запись
                await existing_truck.update(
                    date=dates[i],
                    status=statuses[i]
                ).apply()
            else:
                # Создаём новую запись
                await Trucks.create(
                    truck=plates[i],
                    date=dates[i],
                    status=statuses[i]
                )

    except Exception as e:
        logger.error(f"Ошибка /store_truck_info: {e}")


async def clear_trucks_table():
    try:
        await Trucks.delete.where(True).gino.status()
    except Exception as e:
        print(f"Ошибка /clear_trucks_table: {e}")


async def get_auto_info(plate):
    try:
        plate_upper = plate.upper()
        truck_record = await Trucks.query.where(Trucks.truck == plate_upper).gino.first()

        if truck_record:
            info = (f"╔ 🚛 Номер тягача: {truck_record.truck}\n"
                    f"╠ ⌛️ Дата: {truck_record.date}\n"
                    f"╚ ⚙️ Статус: {truck_record.status}\n")
        else:
            info = NO_CAR_INFO
        return info

    except Exception as e:
        logger.error(f"Ошибка /get_auto_info: {e}")
        return DATA_GET_ERROR


async def get_dates_to_check():
    try:
        dates = []
        forms = await Forms.query.gino.all()
        for form in forms:
            new_date = form.date.replace('.', '')
            date = ((new_date[4] + new_date[5] + new_date[6] + new_date[7]) +
                    (new_date[2] + new_date[3]) + (new_date[0] + new_date[1]))
            dates.append(date)
        return dates
    except Exception as e:
        logger.error(f"Ошибка /get_dates_to_check: {e}")
        return []


async def take_info_via_date(date: str):
    try:
        good_date = f"{date[6:8]}.{date[4:6]}.{date[0:4]}"
        form = await Forms.query.where(Forms.date == good_date).gino.first()
        return [form.truck, form.trailer, form.trans_type, form.trans_species, form.date]
    except Exception as e:
        logger.error(f'Ошибка в /take_info_via_date: {e}')
        return []
