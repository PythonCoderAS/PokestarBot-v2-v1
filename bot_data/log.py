import logging.handlers
import os
from typing import List


class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__("[%(asctime)s] (%(specialformat)s) %(levelname)s: %(message)s")

    def format(self, record: logging.LogRecord) -> str:
        if "bot_data" in record.name:
            record.specialformat = (
                record.name.replace(".", "/") + ".py:" + str(record.lineno)
            )
        else:
            record.specialformat = record.name
        return super().format(record)


def setup_logging(name: str) -> List[str]:
    """
    Sets up the logging for the bot.
    :param name: The name of the logger
    :type name: str
    :return: No return
    :rtype: None
    """
    loggers_modified = []

    logger = logging.getLogger(name)

    base = os.path.abspath(os.path.join(__file__, "..", "..", "logs"))
    os.makedirs(base, exist_ok=True)

    if not os.getenv("NO_DELETE_LOGFILES", ""):
        handler = logging.FileHandler(
            os.path.join(base, "bot.log"), encoding="utf-8", mode="w"
        )
    else:
        handler = logging.FileHandler(os.path.join(base, "bot.log"), encoding="utf-8")

    formatter = CustomFormatter()

    level = os.getenv("LOG_LEVEL", "INFO")
    log_level = getattr(logging, level)
    logger.setLevel(log_level)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logger.addHandler(handler)

    loggers_modified.append(name)

    logging.captureWarnings(True)

    aiosqlite_logger = logging.getLogger("aiosqlite")
    aiosqlite_logger.handlers = []
    aiosqlite_logger.addHandler(logging.NullHandler())

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.WARNING)
    discord_logger.addHandler(handler)

    loggers_modified.append("discord")

    warning_logger = logging.getLogger("py.warnings")
    warning_logger.setLevel(logging.WARNING)
    warning_logger.addHandler(handler)

    loggers_modified.append("py.warnings")

    if os.getenv("LOG_ORM_SQL"):
        tortoise_logger = logging.getLogger("db_client")
        tortoise_logger.setLevel(logging.DEBUG)
        tortoise_logger.addHandler(handler)

        loggers_modified.append("tortoise")

    return loggers_modified
