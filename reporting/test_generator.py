from typing import Any
import re
class TestGenerator:
    """
    -- Test-stub genertor in order to any type of failed conditions like
       -type-mismatch
       -Pre-condition fail
       -Post-condition fail
    """
    def __init__(self, func_name: str,arg_name:str,arg_val:Any, location: str, condition:str) -> None:
        self.func_name = func_name
        self.arg_name=arg_name
        self.arg_val=repr(arg_val)
        self.location = location
        self.condition = re.sub(rf"\b{re.escape(self.arg_name)}\b",self.arg_val, condition)
    
    def __str__(self) -> str:
        test_stub = f"\n#[Test Suggestion]\ndef test_{self.func_name}_{self.location}():\n   result={self.func_name}({self.arg_val})\n   assert {self.condition}\n"
        return test_stub
        