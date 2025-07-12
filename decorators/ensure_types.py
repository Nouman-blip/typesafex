# @ensure_types decorator logic

'''
The decorator function. when it runs, TypeSafeX checks if arguments and types
matche exact annonations. if not, it logs or blocks the execution depending on
mode.
'''
from contracts.type_checker import TypeChecker
from contracts.violations import Violation
from core.engine import Engine
from functools import wraps
import contextvars

# create a mode context for mode
def ensure_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        engine=Engine()
        # calling function 
        violations=[]
        result = func(*args, **kwargs)
        # validate the function types and return
        violation_ = TypeChecker.validate_func_types_and_return(func, *args,result=result, **kwargs)
        for arg, violation_list in violation_.items():
            violations.append(Violation(
                func=func.__name__,
                arg_name=arg,
                arg_val=violation_list[0],
                condition="type mismatch",
                reason=violation_list[1],
                location='type_checker',
                args=args,
                kwargs=kwargs
            ))
            
        engine.handle_violations(func.__name__,violations)
        return result
    return wrapper

        
