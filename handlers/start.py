import logging
from aiogram import types

from lang.texts import *

logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message):
    try:
        await message.answer(START_HELP_TEXT)
    except Exception as ex:
        await message.answer(ERROR_AUTHORIZATION)
        logger.error(f'Ошибка /cmd_start: {ex}.')
