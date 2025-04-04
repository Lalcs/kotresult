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
