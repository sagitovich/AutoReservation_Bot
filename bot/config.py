import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    BOT_TOKEN = os.getenv('MERCURY_BOT_TOKEN')
    BOT_URL = os.getenv('MERCURY_BOT_URL')

    admin_id_str = os.getenv('ADMIN_CHAT_ID', '')
    ADMIN_CHAT_ID = list(map(int, admin_id_str.split(',')))

    AUTO_LIST_URL = os.getenv('AUTO_LIST_URL')
    CHECK_DATES_JSON = os.getenv('CHECK_DATES_JSON')
    AUTHORIZATION_URL = os.getenv('AUTHORIZATION_URL')

    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    PLATE_PATTERN = re.compile(r'^[A-Z]\d{3}[A-Z]{2}\d{2,3}$')
    TRAILER_PATTERN = re.compile(r'^[A-Z]{2}\d{6}$')
    DATE_PATTERN = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')

    IP = os.getenv('IP')
    PGUSER = str(os.getenv('PGUSER'))
    PGPASSWORD = str(os.getenv('PGPASSWORD'))
    DATABASE = str(os.getenv('DATABASE'))
    POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'
