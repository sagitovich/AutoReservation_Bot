import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import Config
from db.db_gino import dataBase
import handlers.start as start
import handlers.upd as upd
import handlers.auto as auto
import handlers.form as form
import handlers.plate as plate

logger = logging.getLogger(__name__)
bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    await bot.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Справка"),
            BotCommand(command="/upd", description="Обновить данные"),
            BotCommand(command="/form", description="Управление заявками"),
            BotCommand(command="/auto", description="Статус тягача")
        ],
        scope=BotCommandScopeDefault()
    )
    dp.message.register(start.cmd_start, Command(commands=['start']))
    dp.message.register(upd.cmd_upd, Command(commands=['upd']))
    dp.message.register(auto.cmd_auto, Command(commands=['auto']))
    dp.message.register(form.cmd_form, Command(commands=['form']))
    dp.message.register(plate.cmd_plate, lambda message: Config.PLATE_PATTERN.match(message.text.upper()))
    dp.message.register(form.push_form, lambda message: message.text.startswith('/plus'))
    dp.message.register(form.edit_date, lambda message: message.text.startswith('/date'))

    dp.callback_query.register(form.callback_add_form, lambda c: c.data == 'add_form')
    dp.callback_query.register(form.callback_edit_form, lambda c: c.data == 'edit_form')
    dp.callback_query.register(form.callback_delete_form, lambda c: c.data == 'delete_form')
    dp.callback_query.register(form.callback_pop_form, lambda c: c.data.startswith('pop_'))
    dp.callback_query.register(form.callback_back_to_variable, lambda c: c.data == 'back_to_variable')

    await dataBase.set_bind(Config.POSTGRES_URI)
    await dataBase.gino.create_all()
    logger.info("Таблицы созданы.")
    await dp.start_polling(bot)
