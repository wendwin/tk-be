import os
import logging
from logging.handlers import RotatingFileHandler


def init_logger(app):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10240,
        backupCount=10
    )

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s "
        "[%(pathname)s:%(lineno)d] : %(message)s"
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Logger initialized")