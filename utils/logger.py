import logging
from enum import Enum, auto
from contextlib import contextmanager
from selenium.common.exceptions import WebDriverException

 # позволяет задать направление вывода. В стандартный вывод, в стандартный вывод и файл
class Output(Enum):
    ConsoleOutput        = auto
    ConsoleAndFileOutput = auto

# функция создания логгера
def get_logger(logger_name: str, level, handler_type: Output, filename = None):
    logger = logging.getLogger(logger_name)

    def add_handler_to_logger(handler_):
        formatter_ = logging.Formatter(f'[%(asctime)s] %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        handler_.setLevel(level)
        handler_.setFormatter(formatter_)
        logger.addHandler(handler_)

    if handler_type is Output.ConsoleAndFileOutput:
        assert filename, f"filename length must be more zero. Filename: {filename}"

        handler = logging.FileHandler(filename)

        add_handler_to_logger(handler)

    elif handler_type is Output.ConsoleOutput:
        pass

    # общий лог
    common_log     = logging.FileHandler("logs/common.log")
    add_handler_to_logger(common_log)

    stream_handler = logging.StreamHandler()
    add_handler_to_logger(stream_handler)
    return logger


 # контекстный менеджер позволяющий перехватывать ошибки позвникающие во время парсинга
@contextmanager
def catch_errors_to_log(logger, msg):
    try:
        yield
    except WebDriverException as ex:
        logger.error(f"{ex} {msg}")
