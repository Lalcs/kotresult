import unittest

from kotresult import run_catching


class TestRunCatching(unittest.TestCase):
    def test_successful_function(self):
        """Test run_catching with a function that succeeds"""

        def successful_function():
            return "success"

        result = run_catching(successful_function)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_none(), "success")

    def test_function_with_args(self):
        """Test run_catching with a function that takes arguments"""

        def add(a, b):
            return a + b

        result = run_catching(add, 2, 3)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_none(), 5)

    def test_function_with_kwargs(self):
        """Test run_catching with a function that takes keyword arguments"""

        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = run_catching(greet, "World")
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_none(), "Hello, World!")

        result = run_catching(greet, name="Python", greeting="Hi")
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_none(), "Hi, Python!")

    def test_function_that_raises_exception(self):
        """Test run_catching with a function that raises an exception"""

        def failing_function():
            raise ValueError("Something went wrong")

        result = run_catching(failing_function)
        self.assertTrue(result.is_failure)
        self.assertIsInstance(result.exception_or_none(), ValueError)
        self.assertEqual(str(result.exception_or_none()), "Something went wrong")

    def test_function_that_raises_different_exception(self):
        """Test run_catching with a function that raises a different type of exception"""

        def division_by_zero():
            return 1 / 0

        result = run_catching(division_by_zero)
        self.assertTrue(result.is_failure)
        self.assertIsInstance(result.exception_or_none(), ZeroDivisionError)

    def test_lambda_function(self):
        """Test run_catching with a lambda function"""
        result = run_catching(lambda x: x * 2, 5)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_none(), 10)
