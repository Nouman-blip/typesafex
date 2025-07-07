# @ensure_types decorator logic

'''
The decorator function. when it runs, TypeSafeX checks if arguments and types
matche exact annonations. if not, it logs or blocks the execution depending on
mode.
'''
from contracts.type_checker import TypeChecker
from core.engine import Engine
from functools import wraps
import contextvars

# create a mode context for mode
def ensure_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        engine=Engine()
        # calling function 
        args_violations=TypeChecker.validate_args(func,*args,**kwargs)
        result = func(*args, **kwargs)
        return_violations=TypeChecker.validate_return(func,result)
        metadata = {
            "func_name": func.__name__,
            "args": args,
            "kwargs": kwargs,
            "return_value":result
        }
        # called and passed the args
        engine.handle_type_violations(metadata,args_violations,return_violations)
        return result
    return wrapper

        
