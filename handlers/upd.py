import logging
from aiogram import types

from bot import bot_init
from bot.config import Config
from lang.texts import *
from functions.authorization import authorization

logger = logging.getLogger(__name__)


async def cmd_upd(message: types.Message):
    try:
        if message.from_user.id in Config.ADMIN_CHAT_ID:
            msg = await message.answer(WAIT_AUTHORIZATION)
            await authorization(Config.LOGIN, Config.PASSWORD)
            await bot_init.bot.edit_message_text(text=SUCCESSFUL_AUTHORIZATION,
                                                 chat_id=message.from_user.id, message_id=msg.message_id)
        else:
            await message.answer(DENIED_ACCESS)
    except Exception as ex:
        await message.answer(ERROR_AUTHORIZATION)
        logger.error(f'Ошибка /cmd_auth: {ex}.')
