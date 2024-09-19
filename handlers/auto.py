import logging
from aiogram import types

from lang.texts import *

logger = logging.getLogger(__name__)


async def cmd_auto(message: types.Message):
    try:
        await message.answer(CHECK_AUTO_PLATE)
    except Exception as ex:
        await message.answer(DATA_GET_ERROR)
        logger.error(f'Ошибка /cmd_auto: {ex}.')
