import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
    )

    file_handler = RotatingFileHandler(
        'logs/bot.log',
        maxBytes=5*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)

    logging.info("Logging system initialized")