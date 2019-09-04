import logging
from logger import get_logger

log = get_logger('MAIN PAGE', logging.INFO)


def speak(phrase=""):
    log.info(f'I say "{phrase}"')


def sing(song=""):
    log.critical(f'I\'m singing "{song}"')


speak('OK')
sing('lalala')
