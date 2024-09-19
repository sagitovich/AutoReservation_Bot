import logging
import sqlalchemy
from gino import Gino
from typing import List

from bot.config import Config

dataBase = Gino()
logger = logging.getLogger(__name__)


class BaseModel(dataBase.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sqlalchemy.Table = sqlalchemy.inspect(self.__class__)
        primary_key_columns: List[sqlalchemy.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


async def on_startup():
    await dataBase.set_bind(Config.POSTGRES_URI)
