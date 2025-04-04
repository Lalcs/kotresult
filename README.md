# kotresult

[![image](https://img.shields.io/pypi/v/kotresult.svg)](https://pypi.org/project/kotresult/)
[![image](https://img.shields.io/pypi/l/kotresult.svg)](https://pypi.org/project/kotresult/)
[![image](https://img.shields.io/pypi/pyversions/kotresult.svg)](https://pypi.org/project/kotresult/)
[![image](https://img.shields.io/github/contributors/lalcs/kotresult.svg)](https://github.com/lalcs/kotresult/graphs/contributors)
[![image](https://img.shields.io/pypi/dm/kotresult)](https://pypistats.org/packages/kotresult)
![Unittest](https://github.com/Lalcs/kotresult/workflows/Unittest/badge.svg)

A Python implementation of the Result monad pattern, inspired by Kotlin's Result class. This library provides a way to
handle operations that might succeed or fail without using exceptions for control flow.

## Installation

You can install the package via pip:

```bash
pip install kotresult
```

## Usage

### Result Class

The `Result` class represents an operation that might succeed or fail. It can contain either a successful value or an
exception.

```python
from kotresult import Result

# Create a success result
success = Result.success("Hello, World!")
print(success.is_success)  # True
print(success.get_or_none())  # "Hello, World!"

# Create a failure result
failure = Result.failure(ValueError("Something went wrong"))
print(failure.is_failure)  # True
print(failure.exception_or_none())  # ValueError("Something went wrong")
```

#### Getting Values Safely

```python
# Get the value or a default
value = success.get_or_default("Default value")  # "Hello, World!"
value = failure.get_or_default("Default value")  # "Default value"

# Get the value or throw the exception
try:
    value = failure.get_or_throw()  # Raises ValueError("Something went wrong")
except ValueError as e:
    print(f"Caught exception: {e}")

# Throw on failure
success.throw_on_failure()  # Does nothing
try:
    failure.throw_on_failure()  # Raises ValueError("Something went wrong")
except ValueError as e:
    print(f"Caught exception: {e}")
```

### run_catching Function

The `run_catching` function executes a function and returns a `Result` object containing either the return value or any
exception that was raised.

```python
from kotresult import run_catching


# With a function that succeeds
def add(a, b):
    return a + b


result = run_catching(add, 2, 3)
print(result.is_success)  # True
print(result.get_or_none())  # 5


# With a function that fails
def divide(a, b):
    return a / b


result = run_catching(divide, 1, 0)  # ZeroDivisionError
print(result.is_failure)  # True
print(type(result.exception_or_none()))  # <class 'ZeroDivisionError'>


# With keyword arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


result = run_catching(greet, name="World", greeting="Hi")
print(result.get_or_none())  # "Hi, World!"
```

## API Reference

### Result Class

#### Static Methods

- `Result.success(value)`: Creates a success result with the given value
- `Result.failure(exception)`: Creates a failure result with the given exception

#### Properties

- `is_success`: Returns `True` if the result is a success, `False` otherwise
- `is_failure`: Returns `True` if the result is a failure, `False` otherwise

#### Methods

- `get_or_none()`: Returns the value if success, `None` if failure
- `exception_or_none()`: Returns the exception if failure, `None` if success
- `to_string()`: Returns a string representation of the result
- `get_or_default(default_value)`: Returns the value if success, the default value if failure
- `get_or_throw()`: Returns the value if success, throws the exception if failure
- `throw_on_failure()`: Throws the exception if failure, does nothing if success

### run_catching Function

- `run_catching(func, *args, **kwargs)`: Executes the function with the given arguments and returns a `Result` object

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
