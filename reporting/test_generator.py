
from typing import Any
class TestGenerator:
    """
    -- Test-stub genertor in order to any type of failed conditions like
       -type-mismatch
       -Pre-condition fail
       -Post-condition fail
    """
    def __init__(self, func_name: str,arg_val:Any, location: str, reason:str) -> None:
        self.func_name = func_name
        self.arg_val=arg_val
        self.location = location
        self.reason=reason
    
    def __str__(self) -> str:
        test_stub = f"\n#[Test Suggestion]\ndef test_{self.func_name}_{self.location}():\n   result={self.func_name}({self.arg_val})\n   assert {self.reason}\n"
        return test_stub
        