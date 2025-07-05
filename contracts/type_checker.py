from typing import (Callable, Any, List, Dict, Optional, Union, Tuple, Set, get_origin, get_args )
import inspect

class TypeChecker:
    """
    -validate the function args
    -validate the return 
    """
    @staticmethod
    def _valid_type(value:Any, expected_type: type) -> bool:
        """
        Validate any type even advance type hints e.g List,Dict, Tuple,Optional,Union
        Args:
          value: Any value could be str, list,dict,tuple,set
          expected_type: type of expected value
        return:
            bool: True or False
        """

        origin = get_origin(expected_type)  # origin will None if expected is class type otherwise typing.Union etc.
        args = get_args(expected_type)  # args will () empty if expected type is class type other wise of typing  args(<'class',str>,...)
        
        # handle Optional[X] which is Union[X,NoneType]
        if origin is Union and type(None) in args:
            # extract non none args
            non_none_args = [arg for arg in args if arg is not type(None)]
            # aceept None or any of the non-none-args
            if value is None:
                return True
            return any(TypeChecker._valid_type(value, arg) for arg in non_none_args)
        
        # handle Union[X,Y,..]
        if origin is Union:
            return any(TypeChecker._valid_type(value, arg) for arg in args)
        
        # handle List[X]
        if origin in (list, List):
            if not isinstance(value, list):
                return False
            if not args:
                return True
            return all(TypeChecker._valid_type(value, arg[0]) for arg in args)
        
        #handle Dict[K,V]
        if origin in (dict, Dict):
            if not isinstance(value, dict):
                return False
            if not args:
                return True
            key_type, val_type=args    
            return all(TypeChecker._valid_type(key_type, k) and TypeChecker._valid_type(val_type, v) for k, v in value.items())  #e.g: {"say":['opps',4]}
        
        #handle Any
        if expected_type is Any:
            return True
        
        # handle Set[X]
        if origin in (set, Set):
            if not isinstance(value, set):
                return False
            if not args:
                return True
            return all(TypeChecker._valid_type(value, arg) for arg in args)
            
        # handle Tuple[T1,T2,...]
        if origin in (tuple, Tuple):
            if not isinstance(value, tuple):
                return False
            if not args:
                return True
            # handle variable length Tuple[T1,...]
            if len(args) == 2 and args[1] is Ellipsis:
                # varaible but same type could be any length of variable like Tupel[int,...] (1,2,4,8,.,.,.)
                return all(TypeChecker._valid_type(item, arg[0]) for item in value)
            # fixed length 
            if len(args) != len(value):
                return False
            return all(TypeChecker._valid_type(item,type_) for item, type_ in zip(value,args) )
        
        # handle custom generic classes or fallback
        if origin is not None:
            # for custom generic classes, fallback to isinstance _valid on origin
               """
               generic classes are parameterized by one or more types using TypeVar and Generic to use any type without
               any duplicate code and also ensure type safety constraints.
               like e.g 
               T=TypeVar('T')
               class Box(Generic(T)):
                PASS
                function(a:Box[int])

               """
            try:
                return isinstance(value, origin)
            except TypeError:
                return True
        
        # handle base class: expected type is class/type means if origin is None
        try:
            return isinstance(value, expected_type)
        except TypeError:
            # sometime expected type is not a class.
            return True



    @staticmethod
    def validate_args(func:Callable,*args:Any,**kwargs:Any)->List:
        """
        using the inspect signature tool to validate the args of a function
        Args:
           func: function to _valid its argument 
           *args: positional arguments of the function
           **kwargs: keyword arguments of the function
        
        return: 
            violtations: List of violation occure for this function
        """
        sig = inspect.signature(func)
        # bound the arguments as correct maping like in tuple which belong 
        bound = sig.bind(*args, **kwargs)
        annotations=func.__annotations__ 
        
        violations = []
        for name, value in bound.arguments.items():
            if name in annotations:
                expected = annotations[name]  
                if not TypeChecker._valid_type(value, expected):
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