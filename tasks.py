from invoke import task, Task
from logger import get_logger
from decorator import invoke2mongo

logger = get_logger('INVOKE TASK', 10)

class GCTask(Task):
    def argspec(self, body):
        # Handle decorated task functions
        # if hasattr(body, '__wrapped__'):
        #     return self.argspec(body.__wrapped__)
        return super().argspec(body)


@task
@invoke2mongo
def say_hello(ctx, name, age):
    logger.info(f'Hello, {name}. Im {age} years old')
