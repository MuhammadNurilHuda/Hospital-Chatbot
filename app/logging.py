# app\logging.py

import logging.config
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__),'..', 'configs', 'logging.conf')

logging.config.fileConfig(CONFIG_PATH)
logger = logging.getLogger('hospital_chatbot')

def log_message(message: str, level: str = "INFO"):
    """
    Mencatat pesan log menggunakan konfigurasi eksternal.
    
    Parameter:
    - message: Pesan yang ingin dicatat.
    - level: Level log ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    """
    if level.upper() == "DEBUG":
        logger.debug(message)
    elif level.upper() == "INFO":
        logger.info(message)
    elif level.upper() == "WARNING":
        logger.warning(message)
    elif level.upper() == "ERROR":
        logger.error(message)
    elif level.upper() == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(message)