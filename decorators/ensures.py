# @enusres decorator logic

'''
you define what must be true after function execution e.g, @ensures(balance>=0)
if violated, you get a detailed report.
'''
from functools import wraps
from contracts.violations import Violation
from core.engine import Engine
import contextvars
def ensures(*conditions):
    def ensures_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            engine=Engine()
    
            result = func(*args, **kwargs)
            violations = []
            # loop over the conditions and checking if violate the function post condition
            # format of conditions is tupe()
            for label, condition in conditions:
                try:
                    if not condition(result):
                        violations.append(Violation(
                            func = func.__name__,
                            reason = f"Post-condtion failed: {label}",
                            location="return"
                        ))
                    
                except Exception as e:
                    violations.append(Violation(
                        func=func.__name__,
                        reason=f"Error in post-condition: {e}",
                        location="return"
                    ))
            engine.handle_violation(func.__name__, violations)
            return result
        return wrapper
    return ensures_decorator
        