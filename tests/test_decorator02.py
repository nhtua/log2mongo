import unittest
import logging

from config import MONGO_COLLECTION
from decorator import log2mongo
from mongo import db
from logger import get_logger


class MyTesteeClass(object):
    @log2mongo()
    def some_func(self):
        logger = get_logger('MY_TESTEE', logging.DEBUG)
        logger.info('what ever message')

    @log2mongo()
    def func_with_params(self, name, age=18):
        logger = get_logger('MY_TESTEE', logging.DEBUG)
        logger.info(f"I'm {name}. I'm {age} years old")


def is_all_in(keywords, text):
    return all([k in text for k in keywords])

class TestDecorator02(unittest.TestCase):
    def setUp(self):
        db[MONGO_COLLECTION].delete_many({})

    def test_log2mongo_for_class(self):
        my_testee  = MyTesteeClass()
        my_testee.some_func()
        log = db[MONGO_COLLECTION].find_one({"input.method":"some_func"})
        assert log              , 'There should be a log in Mongo'
        assert log['timestamp'] , 'Log should have timestamp'
        assert log['input']     , 'Log should have input data'
        assert log['output']    , 'Log should have output data'
        assert log['output']['log_name']  == 'MY_TESTEE', 'log2mongo should keep the right Log Name'
        assert log['output']['log_level'] == 'INFO', 'log2mongo should keep the right Log level'
        assert log['output']['pathname']  == __file__, 'log2mongo should keep the right path of running file'
        assert log['output']['message']   == 'what ever message', 'log2mongo should keep the right Log message'
        assert log['input']['method']     == 'some_func', 'log2mongo should keep right running method name'
        assert is_all_in(['MyTesteeClass object'], log['input']['args']), 'log2mongo should keep the right input args'
        assert '{}' in log['input']['kwargs'], 'log2mongo should keep the right input kwargs'

    def test_function_with_args(self):
        my_testee  = MyTesteeClass()
        my_testee.func_with_params('Tua')
        log = db[MONGO_COLLECTION].find_one({"input.method" : "func_with_params"})
        assert log , 'There should be a log in Mongo'
        assert is_all_in(['MyTesteeClass object', 'Tua'], log['input']['args']) , 'log2mongo should keep the right input args as String'
        assert '{}' in log['input']['kwargs'] , 'log2mongo should keep the right input kwargs'

    def test_function_with_kwargs(self):
        my_testee  = MyTesteeClass()
        my_testee.func_with_params('Tua', age=28)
        log = db[MONGO_COLLECTION].find_one({"input.method" : "func_with_params"})
        assert log , 'There should be a log in Mongo'
        assert is_all_in(['MyTesteeClass object', 'Tua'], log['input']['args']) , 'log2mongo should keep the right input args as String'
        assert '{\'age\': 28}' in log['input']['kwargs'] , 'log2mongo should keep the right input kwargs'

if __name__ == '__main__':
    unittest.main()
