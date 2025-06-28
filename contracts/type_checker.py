from typing import Callable, Any, List
import inspect

class TypeChecker:
    """
    -validate the function args
    -validate the return 
    """

    @staticmethod
    def validate_args(func:Callable,*args:Any,**kwargs:Any)->List:
        """
        using the inspect signature tool to validate the args of a function
        Args:
           func: function to check its argument 
           *args: positional arguments of the function
           **kwargs: keyword arguments of the function
        
        return: 
            violtations: List of violation occure for this function
        """
        sig = inspect.signature(func)
        # bound the arguments as correct maping like in tuple which belong 
        bound = sig.bind(*args, **kwargs)
        annotations=func.__annotations__ # e.g {'a':'<class,str>',...}
        
        violations = []
        for name, value in bound.arguments.items():
            if name in annotations:
                expected = annotations[name]  # e.g '<class,str>'
                if not isinstance(value, expected):
                    violations.append(f"'{name}': expected {expected}, got {type(value)}")
        return violations

    @staticmethod
    def validate_return(func: Callable,result:Any)->str:
        """
        -validate return type
        Args:
           func: func to validate its return
           result: Any type of return value 
        return:
            str: violations statement 
        """
        sig=inspect.signature(func)        
        original_func_return_type = sig.return_annotation
        return_value_type=type(result)
        
        # if no return annotation, skip validation
        if original_func_return_type is inspect.Signature.empty:
            return ""
        
        # check if the result is an instance of the annotated return type
        if not isinstance(result, original_func_return_type):
            return f"{func.__name__}: expected return type {original_func_return_type}, got {type(result)}"
        
        return ""