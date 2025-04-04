from __future__ import annotations

from typing import Generic, TypeVar, Union

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

    def get_or_none(self) -> Union[T, None]:
        if self.is_success:
            return self._value
        return None

    def exception_or_none(self) -> Union[BaseException, None]:
        if self.is_failure:
            return self._value
        return None

    def throw_on_failure(self) -> None:
        if self.is_failure:
            raise self._value

    def get_or_default(self, default_value: R) -> Union[T, R]:
        if self.is_success:
            return self._value
        return default_value

    def get_or_throw(self) -> T:
        if self.is_success:
            return self._value
        raise self._value
