
"""
--
test simplefunc type checker--> greet(name,a): return hi,name
test litte adva type functio--> greet(name:str,a:int): return hi ...
test advanced types like from typing-> greet(name:Optional[str],Dict[List[Any]]): return ...
more with generic type test and all types in typing

flow of this:
@ensure_types 
return return violations and violations with type hints
check if violation from real integeration match with expected test data from conftest
"""
class TestEnsureTypesDecorator:
    """
    Test the ensure_types decorator with various function signatures.
    """
    def test_args_simple_func(self, simple_func):
        """
        Test a simple function with basic type hints.
        """
        expected_violation= 
        assert simple_func("Alice", 42) == ""
        assert simple_func("Bob", 'Hello') == expected_violation
        assert simple_func(42, 42) == expected_violation
    def test_args_advanced_func_simple_type_hints(self, advanced_func_simple_type_hints):
        """
        Test a function with advanced type hints.
        """
        expected_violation = 
        assert advanced_func_simple_type_hints("Alice", 42) == "hi, Alice"
        assert advanced_func_simple_type_hints("Bob", 'Hello') == expected_violation
        assert advanced_func_simple_type_hints(42, 42) == expected_violation