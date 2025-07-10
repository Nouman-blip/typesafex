from decorators.ensure_types import ensure_types
import pytest
class TestEnsureTypesDecorator:
    """
    Test class for the @ensure_types decorator. 
    to test all types of advance or normal functions.
    """
    def test_ensure_types_decorator(self):
        """
        Test the @ensure_types decorator with various function signatures.
        """
        @ensure_types
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3
        assert add(1.0, 2.0) == 3.0
        assert add(1, 2.0) == 3.0

        with pytest.raises(TypeError):
            add("1", "2")
            
    def test_ensure_types_decorator_with_optional(self):
        """
        Test the @ensure_types decorator with functions that have optional parameters.
        """
        @ensure_types
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        assert greet("Alice") == "Hello, Alice!"
        assert greet("Bob", "Hi") == "Hi, Bob!"

        with pytest.raises(TypeError):
            greet(123)
    def test_ensure_types_decorator_with_advance_types(self):
        """
        Test the @ensure_types decorator with functions that have advanced type annotations.
        """
        from typing import List, Dict

        @ensure_types
        def process_data(data: List[Dict[str, int]]) -> int:
            return sum(item['value'] for item in data)

        assert process_data([{"value": 1}, {"value": 2}]) == 3
        assert process_data([{"value": 10}, {"value": 20}]) == 30

        with pytest.raises(TypeError):
            process_data([{"value":"1"}, {"value":"2"}])
    
    def test_ensure_types_decorator_with_union_types(self):
        """
        Test the @ensure_types decorator with functions that have union types.
        """
        from typing import Union

        @ensure_types
        def process_value(value: Union[int, str]) -> str:
            return str(value)

        assert process_value(123) == "123"
        assert process_value("456") == "456"

        with pytest.raises(TypeError):
            process_value(12.34)
    
    def test_ensure_types_decorator_with_nested_types(self):
        """
        Test the @ensure_types decorator with functions that have nested types.
        """
        from typing import List, Tuple

        @ensure_types
        def process_tuples(data: List[Tuple[int, str]]) -> str:
            return ", ".join(f"{num}: {text}" for num, text in data)

        assert process_tuples([(1, "one"), (2, "two")]) == "1: one, 2: two"
        assert process_tuples([(3, "three")]) == "3: three"

        with pytest.raises(TypeError):
            process_tuples([(1, 2), (3, 4)])