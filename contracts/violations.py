
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
        
    def __str__(self):
        return f"[Violation] in {self.func} at {self.location}:{self.reason}"
               