import logging
from logger import get_logger
from decorator import log2mongo


log = get_logger('MAIN PAGE', logging.INFO)

@log2mongo
def speak(phrase=""):
    log.info(f'I say "{phrase}"')
    return phrase

@log2mongo
def sing(song=""):
    log.critical(f'I\'m singing "{song}"')
    log.critical(f'lala la lala')
    return song


speak('OK')
sing('lalala')

