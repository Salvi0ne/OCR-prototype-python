import pytest
# from functools import wraps
from Routes.middleware import auth_middleware

def test_auth_middleware_calls_original_function():
    @auth_middleware
    def example_function(x):
        return x

    result = example_function(42)
    assert result == 42

def test_auth_middleware_raises_exception_if_original_function_raises():
    @auth_middleware
    def example_function():
        raise ValueError("Test exception")
    with pytest.raises(ValueError):
        example_function()
