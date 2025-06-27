# @ensure_types decorator logic

'''
The decorator function. when it runs, TypeSafeX checks if arguments and types
matche exact annonations. if not, it logs or blocks the execution depending on
mode.
'''
from functools import wraps
from core.engine import Engine
def ensure_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # calling function 
        result = func(*args, **kwargs)

        metadata = {
            "func_name": func.__name__,
            "args": args,
            "kwargs": kwargs,
            "return_value":result
        }
        Engine.logger_info(metadata)
        return result
    return wrapper

        
