import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler('avito_bot.log')
logger_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s'
)
logger.addHandler(logger_handler)
logger_handler.setFormatter(logger_formatter)
