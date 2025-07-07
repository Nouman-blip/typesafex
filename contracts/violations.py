from typing import Any

class Violation:
    """
    --handle contract enforcement violations
    """

    def __init__(self,func:str,arg_name:str,arg_val:Any,condition:str,reason:str,location:str,args:Any,kwargs:Any)->None:
        """
        capture violation 
        """
        self.func = func
        self.arg_name=arg_name
        self.arg_val=arg_val
        self.condition=condition
        self.reason = reason
        self.location = location
        self.args = args
        self.kwargs = kwargs
        
        
    def __str__(self)->str:
        return f"[Violation] in {self.func} at  {self.location}, {self.condition} and with arg's name and value {self.arg_name}, {self.arg_val}  with args {self.args} and kwargs {self.kwargs} {self.reason}"
        
    
    
               