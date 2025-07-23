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

# Python naming convention aliases
# get_or_raise() is an alias for get_or_throw()
try:
    value = failure.get_or_raise()  # More Pythonic name
except ValueError as e:
    print(f"Caught exception: {e}")

# raise_on_failure() is an alias for throw_on_failure()
success.raise_on_failure()  # Does nothing
try:
    failure.raise_on_failure()  # More Pythonic name
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

### Advanced Methods

#### Transforming Results with map and mapCatching

```python
from kotresult import Result, run_catching

# map(): Transform success values
result = Result.success(5)
squared = result.map(lambda x: x ** 2)
print(squared.get_or_none())  # 25

# map() on failure returns the same failure
failure = Result.failure(ValueError("error"))
mapped = failure.map(lambda x: x * 2)
print(mapped.is_failure)  # True

# mapCatching(): Transform values and catch exceptions
def risky_transform(x):
    if x > 10:
        raise ValueError("Too large")
    return x * 2

result1 = Result.success(5).map_catching(risky_transform)
print(result1.get_or_none())  # 10

result2 = Result.success(15).map_catching(risky_transform)
print(result2.is_failure)  # True
print(type(result2.exception_or_none()))  # <class 'ValueError'>
```

#### Recovering from Failures

```python
# recover(): Transform failures to successes
failure = Result.failure(ValueError("error"))
recovered = failure.recover(lambda e: "Default value")
print(recovered.get_or_none())  # "Default value"

# recover() on success returns the same success
success = Result.success(42)
recovered = success.recover(lambda e: 0)
print(recovered.get_or_none())  # 42

# recoverCatching(): Recover with exception handling
def risky_recovery(e):
    if "critical" in str(e):
        raise RuntimeError("Cannot recover")
    return "Recovered"

result1 = Result.failure(ValueError("error")).recover_catching(risky_recovery)
print(result1.get_or_none())  # "Recovered"

result2 = Result.failure(ValueError("critical error")).recover_catching(risky_recovery)
print(result2.is_failure)  # True
print(type(result2.exception_or_none()))  # <class 'RuntimeError'>
```

#### Folding Results

```python
# fold(): Handle both success and failure cases with one call
def handle_result(value: str) -> str:
    return parse_int(value).fold(
        on_success=lambda x: f"The number is {x}",
        on_failure=lambda e: f"Invalid input: {e}"
    )

print(handle_result("42"))  # "The number is 42"
print(handle_result("abc"))  # "Invalid input: invalid literal for int() with base 10: 'abc'"

# getOrElse(): Get value or compute alternative from exception
result = parse_int("not_a_number")
value = result.get_or_else(lambda e: len(str(e)))
print(value)  # Length of the error message
```

### Chaining Operations

```python
# Chain multiple transformations
result = (
    run_catching(int, "42")
    .map(lambda x: x * 2)
    .map(lambda x: x + 10)
    .map_catching(lambda x: 100 / x)
)
print(result.get_or_none())  # 1.0526315789473684

# Complex error handling chain
def process_data(data: str) -> str:
    return (
        run_catching(int, data)
        .map(lambda x: x * 2)
        .recover_catching(lambda e: 0)  # Default to 0 on parse error
        .map(lambda x: f"Result: {x}")
        .get_or_else(lambda e: "Processing failed")
    )

print(process_data("21"))  # "Result: 42"
print(process_data("abc"))  # "Result: 0"
```

### run_catching_with Function

The `run_catching_with` function executes a function with a receiver object as the first argument. This is similar to Kotlin's extension function version of runCatching.

**Note**: In Kotlin, there are two versions of `runCatching`:
1. Regular function: `runCatching { ... }`
2. Extension function: `someObject.runCatching { ... }`

Since Python doesn't have extension functions, we implement the extension function version as a separate function called `run_catching_with`, where the receiver object is explicitly passed as the first parameter.

```python
from kotresult import run_catching_with

# Basic usage with string operations
# Kotlin: "hello".runCatching { toUpperCase() }
# Python equivalent:
result = run_catching_with("hello", str.upper)
print(result.get_or_null())  # "HELLO"

# With a custom function
def add_prefix(text, prefix):
    return prefix + text

result = run_catching_with("world", add_prefix, "Hello, ")
print(result.get_or_null())  # "Hello, world"

# With lambda functions
result = run_catching_with(42, lambda x: x * 2)
print(result.get_or_null())  # 84

# Type conversion with error handling
result = run_catching_with("123", int)
print(result.get_or_null())  # 123

result = run_catching_with("not a number", int)
print(result.is_failure)  # True
print(type(result.exception_or_null()))  # <class 'ValueError'>

# Chaining operations with receiver
def process_text(text):
    return text.strip().lower().replace(" ", "_")

result = run_catching_with("  Hello World  ", process_text)
print(result.get_or_null())  # "hello_world"
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

- `get_or_null()`: Returns the value if success, `None` if failure
- `get_or_none()`: Alias for `get_or_null()` for Python naming convention
- `exception_or_null()`: Returns the exception if failure, `None` if success
- `exception_or_none()`: Alias for `exception_or_null()` for Python naming convention
- `to_string()`: Returns a string representation of the result
- `get_or_default(default_value)`: Returns the value if success, the default value if failure
- `get_or_throw()`: Returns the value if success, throws the exception if failure
- `get_or_raise()`: Alias for `get_or_throw()` for Python naming convention
- `throw_on_failure()`: Throws the exception if failure, does nothing if success
- `raise_on_failure()`: Alias for `throw_on_failure()` for Python naming convention
- `on_success(callback)`: Executes the callback with the value if success, returns the Result object for chaining
- `on_failure(callback)`: Executes the callback with the exception if failure, returns the Result object for chaining
- `map(transform)`: Transforms the success value with the given function, returns a new Result
- `map_catching(transform)`: Like map(), but catches exceptions thrown by the transform function
- `recover(transform)`: Transforms the failure exception to a success value, returns a new Result
- `recover_catching(transform)`: Like recover(), but catches exceptions thrown by the transform function
- `fold(on_success, on_failure)`: Applies the appropriate function based on success/failure and returns the result directly (not wrapped in Result)
- `get_or_else(on_failure)`: Returns the success value or computes an alternative value from the exception

### run_catching Function

- `run_catching(func, *args, **kwargs)`: Executes the function with the given arguments and returns a `Result` object

### run_catching_with Function

- `run_catching_with(receiver, func, *args, **kwargs)`: Executes the function with a receiver object as the first argument and returns a `Result` object

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
