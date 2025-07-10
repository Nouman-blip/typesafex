# @no_check decorator logic

'''
it controls runtime contract enforcement. For specific function, it disables 
all runtime contract checks(such as @ensure_types, @requires, @ensures).
'''
from functools import wraps

def no_check(func):
    """
    Decorator to disable runtime contract checks for a specific function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Disable contract checks
        return func(*args, **kwargs)
    return wrapper
    