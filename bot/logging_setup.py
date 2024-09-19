import logging
import os

from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=3
    )
    file_handler.suffix = "%d-%m-%Y"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] | %(name)s | %(levelname)s | %(message)s"))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter("[%(asctime)s] | %(name)s | %(levelname)s | %(message)s"))

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, stream_handler]
    )

    logging.getLogger("aiogram").setLevel(logging.ERROR)
    logging.getLogger("aiohttp").setLevel(logging.ERROR)
    logging.getLogger("aiogram.dispatcher").setLevel(logging.ERROR)
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("selenium").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("gino").setLevel(logging.ERROR)

    logging.info("Логирование настроено.")
