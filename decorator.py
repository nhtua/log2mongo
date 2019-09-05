
from testfixtures import LogCapture

def log2mongo(func):
    def wrapper(*args, **kwargs):
        with LogCapture() as root_log:
            returned_value = func(*args, **kwargs)
        # log something here to MongoDB
        print(f'>>> Start pushing to MongoDB')
        print(root_log.records)
        print(f'>>> End pushing to MongoDB')
        return returned_value
    return wrapper
