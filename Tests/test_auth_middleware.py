import pytest
from functools import wraps
from Routes.middleware import auth_middleware

def test_auth_middleware_calls_original_function():
    @auth_middleware
    def example_function(x):
        return x

    result = example_function(42)
    assert result == 42

def test_auth_middleware_passes_args():
    @auth_middleware
    def example_function(x, y):
        return x + y

    result = example_function(2, 3)
    assert result == 5

def test_auth_middleware_passes_kwargs():
    @auth_middleware
    def example_function(x, y=None):
        return x if y is None else x + y

    result = example_function(2, y=3)
    assert result == 5

def test_auth_middleware_raises_exception_if_original_function_raises():
    @auth_middleware
    def example_function():
        raise ValueError("Test exception")
    with pytest.raises(ValueError):
        example_function()
