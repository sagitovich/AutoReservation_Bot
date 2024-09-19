import logging
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import bot_init
from bot.config import Config
from lang.texts import FORM_TEXT, HELP_TEXT, HELP_TEXT_EDIT
from db.commands import add_form, rewrite_date, delete_form
from handlers.keyboards import (list_of_forms, forms_variables_keyboards, forms_variable_to_add,
                                forms_variable_to_delete)

logger = logging.getLogger(__name__)
# global msg


async def generate_text():
    try:
        text = ''
        all_forms = await list_of_forms()
        for form in all_forms:
            form_id, truck, trailer, trans_type, trans_species, special_cargo, date = form
            text += FORM_TEXT.format(form_id, truck, trailer if trailer else 'не указан', trans_type, trans_species,
                                     special_cargo if special_cargo else 'не указан', date)
        return text
    except Exception as e:
        logger.warning(f'Предупреждение /generate_text: {e}')
        return '<b>Нет сохранённых заявок!</b>'


async def cmd_form(message: types.Message, state: FSMContext):
    try:
        text = await generate_text()
        msg = await message.answer(text=text, reply_markup=await forms_variables_keyboards())
        await state.update_data(msg=msg)
    except Exception as e:
        logger.error(f'Ошибка /cmd_form: {e}')


async def callback_add_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")

    await bot_init.bot.edit_message_text(text=HELP_TEXT, reply_markup=await forms_variable_to_add(),
                                         chat_id=call.from_user.id, message_id=msg.message_id)
    await call.answer(text='Для создания заявки напишите её и отправьте...', cache_time=10)


async def push_form(message: types.Message):
    user_form = message.text[6:]
    form_lines = user_form.split('\n')

    if len(form_lines) == 6:

        if len(form_lines[0]) == 8 and Config.PLATE_PATTERN.match(form_lines[0]):
            truck = form_lines[0]
        else:
            await message.answer(f'Неверный номер тягача!')
            return

        if len(form_lines[1]) == 8 and Config.TRAILER_PATTERN.match(form_lines[1]):
            trailer = form_lines[1]
        elif len(form_lines[1]) == 0:
            trailer = ''
        else:
            await message.answer(f'Неверный номер прицепа!')
            return

        if form_lines[2] in ['Экспорт', 'Транзит']:
            trans_type = form_lines[2]
        else:
            await message.answer(f'Неверный тип перевозки!')
            return

        if form_lines[3] in ['Перевозка грузов', 'Порожний']:
            trans_species = form_lines[3]
        else:
            await message.answer(f'Неверный вид перевозки!')
            return

        if len(form_lines[4]) != 0 and form_lines[4] in ['Скоропортящийся груз', 'Живой скот',
                                                         'Опасный груз', 'Другой особый груз']:
            special_cargo = form_lines[4]
        elif len(form_lines[4]) == 0:
            special_cargo = ''
        else:
            await message.answer(f'Неверный тип особого груза!')
            return

        if len(form_lines[5]) != 0 and Config.DATE_PATTERN.match(form_lines[5]):
            date = form_lines[5]
        else:
            await message.answer(f'Неверный формат даты!')
            return

        await add_form(truck, trailer, trans_type, trans_species, special_cargo, date)
        await message.answer(f'Ваша форма заявки сохранена!')

    elif len(form_lines) > 6:
        await message.answer(f'<b>Ошибка!</b>\n'
                             f'Избыточные строки.')
    else:
        await message.answer(f'<b>Ошибка!</b>\n'
                             f'Недостаточно данных для заполнения формы.')


async def callback_edit_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")

    text = await generate_text()
    text += HELP_TEXT_EDIT
    await bot_init.bot.edit_message_text(text=text, reply_markup=await forms_variable_to_add(),
                                         chat_id=call.from_user.id, message_id=msg.message_id)


async def edit_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")

    try:
        user_form = message.text[6:]
        form_lines = user_form.split('\n')
        await rewrite_date(form_id=int(form_lines[0]), date=form_lines[1])

        await bot_init.bot.edit_message_text(text=await generate_text(), reply_markup=await forms_variables_keyboards(),
                                             chat_id=message.from_user.id, message_id=msg.message_id)
        await message.answer(f'Дата заявки №{form_lines[0]} обновлена!')
    except Exception as e:
        logger.error(f'Ошибка /edit_date: {e}')


async def callback_delete_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")

    await bot_init.bot.edit_message_reply_markup(reply_markup=await forms_variable_to_delete(),
                                                 chat_id=call.from_user.id,
                                                 message_id=msg.message_id)


async def callback_pop_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")

    form_id_ = int((str(call.data))[-1])
    await delete_form(form_id=form_id_)
    await bot_init.bot.edit_message_text(text=await generate_text(), reply_markup=await forms_variables_keyboards(),
                                         chat_id=call.from_user.id, message_id=msg.message_id)
    await call.answer(text=f'Заявка №{form_id_} успешно удалена!', cache_time=3)


async def callback_back_to_variable(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data.get("msg")
    # вернуться на выбор действия
    await bot_init.bot.edit_message_text(text=await generate_text(), reply_markup=await forms_variables_keyboards(),
                                         chat_id=call.from_user.id, message_id=msg.message_id)
