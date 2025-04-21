import unittest

from kotresult import Result


class TestResult(unittest.TestCase):
    def test_success_creation(self):
        """Test creating a success Result"""
        result = Result.success("test value")
        self.assertTrue(result.is_success)
        self.assertFalse(result.is_failure)
        self.assertEqual(result.get_or_none(), "test value")
        self.assertIsNone(result.exception_or_none())

    def test_failure_creation(self):
        """Test creating a failure Result"""
        exception = ValueError("test error")
        result = Result.failure(exception)
        self.assertFalse(result.is_success)
        self.assertTrue(result.is_failure)
        self.assertIsNone(result.get_or_none())
        self.assertEqual(result.exception_or_none(), exception)

    def test_to_string(self):
        """Test the to_string method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        self.assertEqual(success_result.to_string(), "Success(test value)")
        self.assertEqual(failure_result.to_string(), "Failure(test error)")
        # The to_string method only includes the string representation of the exception,
        # not the exception type name

    def test_get_or_default(self):
        """Test the get_or_default method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        self.assertEqual(success_result.get_or_default("default"), "test value")
        self.assertEqual(failure_result.get_or_default("default"), "default")

    def test_get_or_throw(self):
        """Test the get_or_throw method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        self.assertEqual(success_result.get_or_throw(), "test value")
        with self.assertRaises(ValueError):
            failure_result.get_or_throw()

    def test_throw_on_failure(self):
        """Test the throw_on_failure method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # Should not raise an exception
        success_result.throw_on_failure()

        # Should raise the stored exception
        with self.assertRaises(ValueError):
            failure_result.throw_on_failure()

    def test_on_success(self):
        """Test the on_success method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # For a success result, the callback should be called
        success_value = None

        def success_callback(value):
            nonlocal success_value
            success_value = value

        result = success_result.on_success(success_callback)
        self.assertEqual(success_value, "test value")
        self.assertIs(result, success_result)  # Should return self for chaining

        # For a failure result, the callback should not be called
        success_value = None
        failure_result.on_success(success_callback)
        self.assertIsNone(success_value)

    def test_on_failure(self):
        """Test the on_failure method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # For a failure result, the callback should be called
        failure_exception = None

        def failure_callback(exception):
            nonlocal failure_exception
            failure_exception = exception

        result = failure_result.on_failure(failure_callback)
        self.assertIsInstance(failure_exception, ValueError)
        self.assertEqual(str(failure_exception), "test error")
        self.assertIs(result, failure_result)  # Should return self for chaining

        # For a success result, the callback should not be called
        failure_exception = None
        success_result.on_failure(failure_callback)
        self.assertIsNone(failure_exception)

    def test_method_chaining(self):
        """Test method chaining with on_success and on_failure"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        success_value = None
        failure_exception = None

        def success_callback(value):
            nonlocal success_value
            success_value = value

        def failure_callback(exception):
            nonlocal failure_exception
            failure_exception = exception

        # Chain methods on a success result
        success_result.on_success(success_callback).on_failure(failure_callback)
        self.assertEqual(success_value, "test value")
        self.assertIsNone(failure_exception)

        # Reset values
        success_value = None
        failure_exception = None

        # Chain methods on a failure result
        failure_result.on_success(success_callback).on_failure(failure_callback)
        self.assertIsNone(success_value)
        self.assertIsInstance(failure_exception, ValueError)
