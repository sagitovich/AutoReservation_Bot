import logging
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.commands import list_of_forms

logger = logging.getLogger(__name__)


async def forms_variables_keyboards():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить форму', callback_data='add_form')],
        [types.InlineKeyboardButton(text='Изменить даты', callback_data='edit_form')],
        [types.InlineKeyboardButton(text='Удалить форму', callback_data='delete_form')]
    ])
    return keyboard


async def forms_variable_to_add():
    try:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Назад', callback_data='back_to_variable')]
        ])
        return keyboard
    except Exception as e:
        logger.error(f'Ошибка /forms_variable_to_add: {e}')


async def forms_variable_to_delete():
    try:
        buttons = []
        all_forms = await list_of_forms()
        for form in all_forms:
            form_id, _, _, _, _, _, _ = form
            text = f'Удалить заявку №{form_id}'
            buttons.append([InlineKeyboardButton(text=text, callback_data=f'pop_{form_id}')])
        buttons.append([InlineKeyboardButton(text='Назад', callback_data='back_to_variable')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    except Exception as e:
        logger.error(f'Ошибка /forms_variable_to_delete: {e}')
