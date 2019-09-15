from functools import update_wrapper, partial, wraps
from testfixtures import LogCapture
import contextlib

from mongo import db
from config import MONGO_COLLECTION


def obj_to_text(obj, default: 'Anything can repr to string' = ''):
    try:
        text = repr(obj)
    except TypeError as e:
        text = repr(default)
    return text

def log2mongo(collection_name=MONGO_COLLECTION):
    class Log2MongoDecorator(object):
        """
        Solution for decorator as class here https://stackoverflow.com/a/45361673/1235074
        """

        def __init__(self, func):
            update_wrapper(self, func)
            self.func = func

        def __get__(self, obj, objtype):
            """Support instance methods."""
            return partial(self.__call__, obj)

        def __call__(self, *args, **kwargs):
            with LogCapture() as root_log:
                returned_value = self.func(*args, **kwargs)
            # log something here to MongoDB
            print(f'>>> Start pushing to MongoDB')
            for log in root_log.records:

                data = {
                    "timestamp": log.asctime,
                    "input": {
                        "method": self.func.__name__,
                        "args": obj_to_text(args, default=[]),
                        "kwargs": obj_to_text(kwargs, default={})
                    },
                    "output": {
                        "log_name" : log.name,
                        "log_level": log.levelname,
                        "pathname" : log.pathname,
                        "message"  : log.message
                    }
                }
                db[collection_name].insert_one(data)
            print(f'>>> End pushing to MongoDB')
            return returned_value
    return Log2MongoDecorator


def invoke2mongo(func):
    @wraps(func)
    def wrapper(context, *args, **kwargs):
        with LogCapture() as root_log:
            returned_value = func(context, *args, **kwargs)
        # log something here to MongoDB
        for log in root_log.records:
            data = {
                "timestamp": log.asctime,
                "input": {
                    "method": func.__name__,
                    "args": obj_to_text(args),
                    "kwargs": obj_to_text(kwargs)
                },
                "output": {
                    "log_name" : log.name,
                    "log_level": log.levelname,
                    "pathname" : log.pathname,
                    "message"  : log.message
                }
            }
            db[MONGO_COLLECTION].insert_one(data)
        return returned_value

    return wrapper


def simple_deco(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print('where am I? inner')
        return func(*args, **kwargs)
    return inner


@contextlib.contextmanager
def capture():
    import sys
    from io import StringIO
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()