import inspect
import types
from itertools import zip_longest
from invoke import task, Task
from invoke.tasks import NO_DEFAULT

from logger import get_logger
from decorator import invoke2mongo, simple_deco

logger = get_logger('INVOKE TASK', 10)

class GCTask(Task):
    """
    I custom this class because of Invoke Task has a problem with other @decorator

    https://github.com/pyinvoke/invoke/pull/399
    https://github.com/pyinvoke/invoke/pull/246
    https://github.com/pyinvoke/invoke/issues/555
    """

    def argspec(self, body):
        """
        The original one is using inspect.getargspec() to get args list
        That was recommended to replace by inspect.signature()
        https://docs.python.org/3.6/library/inspect.html#inspect.getargspec
        """
        sig = inspect.signature(body)
        arg_names = []
        spec_dict = {}
        for param in sig.parameters:
            arg = sig.parameters[param]
            arg_names.append(param)
            spec_dict[param] = NO_DEFAULT if arg.default == inspect._empty else arg.default
        try:
            context_arg = arg_names.pop(0)
        except IndexError:
            raise TypeError("Tasks must have an initial Context argument!")
        del spec_dict[context_arg]
        return arg_names, spec_dict

@task(klass=GCTask)
@invoke2mongo
def say_hello(ctx, name, age=10):
    logger.info(f'Hello, {name}. Im {age} years old')
