from mongo import db
from testfixtures import LogCapture


def log2mongo(func):
    def wrapper(*args, **kwargs):
        with LogCapture() as root_log:
            returned_value = func(*args, **kwargs)
        # log something here to MongoDB
        print(f'>>> Start pushing to MongoDB')
        for log in root_log.records:
            data = {
                "timestamp": log.asctime,
                "input": {
                    "method": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                },
                "output": {
                    "log_name" : log.name,
                    "log_level": log.levelname,
                    "pathname" : log.pathname,
                    "message"  : log.message
                }
            }
            db.auto_logs.insert_one(data)
        print(f'>>> End pushing to MongoDB')
        return returned_value

    return wrapper
