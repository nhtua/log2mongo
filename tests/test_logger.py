import unittest
import logging
from testfixtures import LogCapture

from logger import get_logger


class TestLogger(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger('LOG NAME', logging.DEBUG)
        INP = [
            "some debug",
            "some info",
            "MY MESSAGE",
            "what error?",
            "the critical one",
        ]
        EXP = [
            "LOG NAME", "DEBUG", "some debug",
            "INFO", "some info",
            "WARNING", "MY MESSAGE",
            "ERROR", "what error?",
            "CRITICAL", "the critical one",
        ]
        with LogCapture() as log:
            logger.debug(INP[0])
            logger.info(INP[1])
            logger.warning(INP[2])
            logger.error(INP[3])
            logger.critical(INP[4])

        assert all([text in str(log) for text in EXP])




if __name__ == '__main__':
    unittest.main()
