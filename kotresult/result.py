from __future__ import annotations

from typing import Generic, TypeVar, Union, Callable

T = TypeVar('T')
R = TypeVar('R')


class Result(Generic[T]):
    def __init__(self, value: Union[T, BaseException]):
        self._value = value

    @staticmethod
    def success(value: T) -> Result[T]:
        return Result(value)

    @staticmethod
    def failure(exception: BaseException) -> Result[T]:
        return Result(exception)

    @property
    def is_success(self):
        return not isinstance(self._value, BaseException)

    @property
    def is_failure(self):
        return isinstance(self._value, BaseException)

    def to_string(self) -> str:
        if self.is_success:
            return "Success({})".format(self._value)
        return "Failure({})".format(self._value)

    def get_or_null(self) -> Union[T, None]:
        if self.is_success:
            return self._value
        return None

    def exception_or_null(self) -> Union[BaseException, None]:
        if self.is_failure:
            return self._value
        return None

    # Python naming convention aliases
    def get_or_none(self) -> Union[T, None]:
        """Alias for get_or_null() for Python naming convention"""
        return self.get_or_null()

    def exception_or_none(self) -> Union[BaseException, None]:
        """Alias for exception_or_null() for Python naming convention"""
        return self.exception_or_null()

    def throw_on_failure(self) -> None:
        if self.is_failure:
            raise self._value

    # Python naming convention alias
    def raise_on_failure(self) -> None:
        """Alias for throw_on_failure() for Python naming convention"""
        return self.throw_on_failure()

    def get_or_default(self, default_value: R) -> Union[T, R]:
        if self.is_success:
            return self._value
        return default_value

    def get_or_throw(self) -> T:
        if self.is_success:
            return self._value
        raise self._value

    # Python naming convention alias
    def get_or_raise(self) -> T:
        """Alias for get_or_throw() for Python naming convention"""
        return self.get_or_throw()

    def on_success(self, callback: Callable[[T], None]) -> Result[T]:
        if self.is_success:
            callback(self._value)
        return self

    def on_failure(self, callback: Callable[[BaseException], None]) -> Result[T]:
        if self.is_failure:
            callback(self._value)
        return self

    def map(self, transform: Callable[[T], R]) -> Result[R]:
        if self.is_success:
            return Result.success(transform(self._value))
        return Result.failure(self._value)

    def map_catching(self, transform: Callable[[T], R]) -> Result[R]:
        if self.is_success:
            try:
                return Result.success(transform(self._value))
            except BaseException as e:
                return Result.failure(e)
        return Result.failure(self._value)

    def recover(self, transform: Callable[[BaseException], T]) -> Result[T]:
        if self.is_failure:
            return Result.success(transform(self._value))
        return self

    def recover_catching(self, transform: Callable[[BaseException], T]) -> Result[T]:
        if self.is_failure:
            try:
                return Result.success(transform(self._value))
            except BaseException as e:
                return Result.failure(e)
        return self

    def fold(self, on_success: Callable[[T], R], on_failure: Callable[[BaseException], R]) -> R:
        if self.is_success:
            return on_success(self._value)
        return on_failure(self._value)

    def get_or_else(self, on_failure: Callable[[BaseException], T]) -> T:
        if self.is_success:
            return self._value
        return on_failure(self._value)

    # Python special methods
    def __str__(self) -> str:
        """String representation of the Result"""
        return self.to_string()

    def __repr__(self) -> str:
        """Detailed representation of the Result"""
        if self.is_success:
            return f"Result.success({repr(self._value)})"
        return f"Result.failure({repr(self._value)})"

    def __eq__(self, other) -> bool:
        """Check equality between Results"""
        if not isinstance(other, Result):
            return False
        if self.is_success and other.is_success:
            return self._value == other._value
        if self.is_failure and other.is_failure:
            return type(self._value) == type(other._value) and str(self._value) == str(other._value)
        return False

    def __ne__(self, other) -> bool:
        """Check inequality between Results"""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Hash the Result for use in sets and dicts"""
        if self.is_success:
            return hash(("success", self._value))
        return hash(("failure", type(self._value).__name__, str(self._value)))
