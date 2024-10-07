import logging
import os

def get_logger():
    graylog_host = os.getenv("GRAYLOG_HOST")
    graylog_port = os.getenv("GRAYLOG_PORT")

    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    if graylog_host and graylog_port:
        handler = logging.handlers.SysLogHandler(address=(graylog_host, int(graylog_port)))
        logger.addHandler(handler)

    return logger
