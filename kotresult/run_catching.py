from typing import Callable, TypeVar

from kotresult.result import Result

T = TypeVar('T')


def run_catching(func: Callable[..., T], *args, **kwargs) -> Result[T]:
    try:
        return Result.success(func(*args, **kwargs))
    except BaseException as e:
        return Result.failure(e)
