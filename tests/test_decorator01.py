import unittest
import logging
import io
from contextlib import redirect_stdout

from config import MONGO_COLLECTION
from decorator import log2mongo, CaptureStdout
from mongo import db
from logger import get_logger


class TestDecorator01(unittest.TestCase):
    def setUp(self):
        db[MONGO_COLLECTION].delete_many({})

    def test_log2mongo_returned_value(self):
        def testee(abc):
            return abc

        INP = 'something'
        EXP = testee(INP)
        OUT = log2mongo()(testee)(INP)
        assert EXP == OUT, 'Decorator log2mongo should return exactly the original function'

    def test_log2mongo_in_db(self):
        """
        Make sure log in right format
         data = {
            "timestamp": log.asctime,
            "input": {
                "method": func.__name__,
                "args": args_as_String,
                "kwargs": kwargs_as_String
            },
            "output": {
                "log_name" : log.name,
                "log_level": log.levelname,
                "pathname" : log.pathname,
                "message"  : log.message
            }
        }
        """
        logger = get_logger('DATA_IN_MONGO', logging.DEBUG)
        @log2mongo()
        def testee(abc):
            logger.info(abc)
        testee('some message!')
        log = db[MONGO_COLLECTION].find_one({"input.method":"testee"})
        assert log              , 'There should be a log in Mongo'
        assert log['timestamp'] , 'Log should have timestamp'
        assert log['input']     , 'Log should have input data'
        assert log['output']    , 'Log should have output data'
        assert log['output']['log_name']  == 'DATA_IN_MONGO', 'log2mongo should keep the right Log Name'
        assert log['output']['log_level'] == 'INFO', 'log2mongo should keep the right Log level'
        assert log['output']['pathname']  == __file__, 'log2mongo should keep the right path of running file'
        assert log['output']['message']   == 'some message!', 'log2mongo should keep the right Log message'
        assert log['input']['method']     == 'testee', 'log2mongo should keep right running method name'
        assert log['input']['args']       == repr(('some message!',)), 'log2mongo should keep the right input args'
        assert log['input']['kwargs']     == repr({}) , 'log2mongo should keep the right input kwargs'

    def test_pure_capture(self):
        def lab_mouse(abc):
            logger = get_logger('PURE CAPTURE', level=logging.DEBUG)
            logger.info(f'hello, {abc}')
        with CaptureStdout() as out:
            lab_mouse('some log')
        assert 'some log' in out

    def test_redirect_stdout(self):
        """
        THIS IS THE BEST WAY TO CAPTURE ALL LOG OUTPUT
        """
        def lab_mouse(abc):
            logger = get_logger('REDIRECT_STDOUT', level=logging.DEBUG)
            logger.info(f'hello, {abc}')

        f = io.StringIO()
        with redirect_stdout(f):
            lab_mouse('im here')
        out = f.getvalue()
        assert 'im here' in out

if __name__ == '__main__':
    unittest.main()
