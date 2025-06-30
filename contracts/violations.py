
from typing import Any
class Violation:
    """
    --handle contract enforcement violations
    """

    def __init__(self,func:str,reason:str,location:str)->None:
        """
        capture violation 
        """
        self.func= func
        self.reason = reason
        self.location = location
        
    def __str__(self)->str:
        return f"[Violation] in func_name:{self.func} at location:{self.location}:{self.reason}"
               