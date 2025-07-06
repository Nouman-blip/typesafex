from reporting.test_generator import TestGenerator
from typing import Any

class Violation:
    """
    --handle contract enforcement violations
    """

    def __init__(self,func:str,arg_name:str,arg_val:Any,condition:str,reason:str,location:str)->None:
        """
        capture violation 
        """
        self.func = func
        self.arg_name=arg_name
        self.arg_val=arg_val
        self.condition=condition
        self.reason = reason
        self.location = location
        self.test_stub = TestGenerator(self.func, self.arg_name, self.arg_val, self.location, self.condition)
        
    
        
    def __str__(self)->str:
        return {f"[Violation] in {self.func} at {self.location}, {self.reason}":self.test_stub}
        
    
    
               