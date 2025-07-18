import unittest

from kotresult import run_catching, run_catching_with


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


class TestRunCatchingWith(unittest.TestCase):
    def test_successful_function_with_receiver(self):
        """Test run_catching_with with a function that succeeds"""
        
        def get_length(s):
            return len(s)
        
        result = run_catching_with("hello", get_length)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), 5)
    
    def test_method_call_with_receiver(self):
        """Test run_catching_with with a method call"""
        
        def upper_case(s):
            return s.upper()
        
        result = run_catching_with("hello world", upper_case)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), "HELLO WORLD")
    
    def test_function_with_additional_args(self):
        """Test run_catching_with with additional arguments"""
        
        def add_prefix(s, prefix):
            return prefix + s
        
        result = run_catching_with("world", add_prefix, "Hello, ")
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), "Hello, world")
    
    def test_function_with_kwargs(self):
        """Test run_catching_with with keyword arguments"""
        
        def format_string(s, prefix="", suffix=""):
            return f"{prefix}{s}{suffix}"
        
        result = run_catching_with("Python", format_string, prefix="Hello, ", suffix="!")
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), "Hello, Python!")
    
    def test_lambda_with_receiver(self):
        """Test run_catching_with with a lambda function"""
        
        result = run_catching_with(10, lambda x: x * x)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), 100)
    
    def test_failing_function_with_receiver(self):
        """Test run_catching_with with a function that raises an exception"""
        
        def parse_int(s):
            return int(s)
        
        result = run_catching_with("not a number", parse_int)
        self.assertTrue(result.is_failure)
        self.assertIsInstance(result.exception_or_null(), ValueError)
    
    def test_type_conversion_with_receiver(self):
        """Test run_catching_with for type conversion"""
        
        # Successful conversion
        result = run_catching_with("42", int)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), 42)
        
        # Failed conversion
        result = run_catching_with("abc", int)
        self.assertTrue(result.is_failure)
        self.assertIsInstance(result.exception_or_null(), ValueError)
    
    def test_chaining_with_receiver(self):
        """Test run_catching_with can be used in chains"""
        
        def process_string(s):
            return s.strip().upper()
        
        result = run_catching_with("  hello  ", process_string)
        self.assertTrue(result.is_success)
        self.assertEqual(result.get_or_null(), "HELLO")
