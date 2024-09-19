import logging
from aiogram import types

from lang.texts import *
from db.commands import get_auto_info

logger = logging.getLogger(__name__)


async def cmd_plate(message: types.Message):
    try:
        info = await get_auto_info(message.text.upper())
        await message.answer(text=info)
    except Exception as ex:
        await message.answer(DATA_GET_ERROR)
        logger.error(f'Ошибка /cmd_plate: {ex}.')
