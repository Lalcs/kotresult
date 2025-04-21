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

### Using Result as a Function Return

You can use the `Result` class as a return type for your functions to handle operations that might fail:

```python
from kotresult import Result


# Function that returns a Result
def parse_int(value: str) -> Result[int]:
    try:
        return Result.success(int(value))
    except ValueError as e:
        return Result.failure(e)


# Using the function
result = parse_int("42")
if result.is_success:
    print(f"Parsed value: {result.get_or_none()}")  # Parsed value: 42
else:
    print(f"Failed to parse: {result.exception_or_none()}")

# With a value that can't be parsed
result = parse_int("not_a_number")
if result.is_success:
    print(f"Parsed value: {result.get_or_none()}")
else:
    print(f"Failed to parse: {result.exception_or_none()}")  # Failed to parse: ValueError("invalid literal for int() with base 10: 'not_a_number'")

# You can also chain operations that return Result
def double_parsed_int(value: str) -> Result[int]:
    result = parse_int(value)
    if result.is_success:
        return Result.success(result.get_or_none() * 2)
    return result  # Return the failure result as is


result = double_parsed_int("21")
print(result.get_or_default(0))  # 42

result = double_parsed_int("not_a_number")
print(result.get_or_default(0))  # 0

# Using on_success and on_failure for handling results
def process_result(value: str):
    parse_int(value).on_success(
        lambda x: print(f"Successfully parsed {value} to {x}")
    ).on_failure(
        lambda e: print(f"Failed to parse {value}: {e}")
    )

process_result("42")  # Successfully parsed 42 to 42
process_result("not_a_number")  # Failed to parse not_a_number: invalid literal for int() with base 10: 'not_a_number'
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
- `on_success(callback)`: Executes the callback with the value if success, returns the Result object for chaining
- `on_failure(callback)`: Executes the callback with the exception if failure, returns the Result object for chaining

### run_catching Function

- `run_catching(func, *args, **kwargs)`: Executes the function with the given arguments and returns a `Result` object

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
