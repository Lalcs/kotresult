from typing import Callable, TypeVar

from kotresult.result import Result

T = TypeVar('T')
R = TypeVar('R')


def run_catching(func: Callable[..., T], *args, **kwargs) -> Result[T]:
    try:
        return Result.success(func(*args, **kwargs))
    except BaseException as e:
        return Result.failure(e)


def run_catching_with(receiver: T, func: Callable[..., R], *args, **kwargs) -> Result[R]:
    """
    Execute a function with a receiver object as the first argument.
    This is similar to Kotlin's extension function version of runCatching.
    
    In Kotlin, there are two versions of runCatching:
    1. Regular function: runCatching { ... }
    2. Extension function: someObject.runCatching { ... }
    
    This function implements the equivalent of Kotlin's extension function version,
    where the receiver object is passed as the first argument to the function.
    Since Python doesn't have extension functions, we implement it as a separate function.
    
    Args:
        receiver: The object to pass as the first argument to func
        func: The function to execute with receiver as the first argument
        *args: Additional positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        Result containing either the function's return value or any raised exception
    
    Example:
        # Kotlin: "hello".runCatching { this.toUpperCase() }
        # Python: run_catching_with("hello", str.upper)
    """
    try:
        return Result.success(func(receiver, *args, **kwargs))
    except BaseException as e:
        return Result.failure(e)
