import logging
import os

def get_logger():
    graylog_host = os.getenv("GRAYLOG_HOST")
    graylog_port = os.getenv("GRAYLOG_PORT")

    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    # Define o formato das mensagens de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configura o handler para o Graylog
    if graylog_host and graylog_port:
        handler = logging.handlers.SysLogHandler(address=(graylog_host, int(graylog_port)))
        handler.setFormatter(formatter)  # Aplica o formatador ao handler do Graylog
        logger.addHandler(handler)

    # Handler opcional para console (exibe logs localmente)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
