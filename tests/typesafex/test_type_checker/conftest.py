from decorators.ensure_types import ensure_types
from typing import Optional, Dict, List, Any, TypeVar
import pytest

# simple function to greet(name, a) # with type hints
@pytest.fixture
def simple_func():
    @ensure_types
    def greet(name, a):
        return f"hi, {name}"

    return greet

# function with advanced type hints name: str, a: int
@pytest.fixture
def advanced_func_simple_type_hints() -> str:
    @ensure_types
    def greet(name: str, a: int):
        return f"hi, {name}"

    return greet
# function with advanced type hints name: Optional[str], a: Dict[List[Any]]
@pytest.fixture
def advanced_func_advanced_type_hints():
    @ensure_types
    def greet(name: Optional[str], a: Dict[List[Any]])-> Optional[str]:
        return  [99, 100, 101]

    return greet

# function with generic type hints name: T, a: List[T]
T = TypeVar('T')
@pytest.fixture
def advanced_func_generic_type_hints():
    @ensure_types
    def greet(name: T, a: List[T])-> List[T]:
        return f"hi, {name}"

    return greet

# function with all types from typing
@pytest.fixture
def advanced_func_all_types():
    @ensure_types
    def greet(name: Optional[str], a: Dict[str, List[Any]]) -> Optional[str]:
        return f"hi, {name}"

    return greet

# function with all types from typing with type hints
@pytest.fixture
def advanced_func_all_types_with_type_hints():
    @ensure_types
    def greet(name: Optional[str], a: Dict[str, List[Any]]) -> Optional[str]:
        return f"hi, {name}"

    return greet
