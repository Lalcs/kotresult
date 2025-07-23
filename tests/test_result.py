import unittest

from kotresult import Result


class TestResult(unittest.TestCase):
    def test_success_creation(self):
        """Test creating a success Result"""
        result = Result.success("test value")
        self.assertTrue(result.is_success)
        self.assertFalse(result.is_failure)
        self.assertEqual(result.get_or_null(), "test value")
        self.assertIsNone(result.exception_or_null())

    def test_failure_creation(self):
        """Test creating a failure Result"""
        exception = ValueError("test error")
        result = Result.failure(exception)
        self.assertFalse(result.is_success)
        self.assertTrue(result.is_failure)
        self.assertIsNone(result.get_or_null())
        self.assertEqual(result.exception_or_null(), exception)

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

        # Test that get_or_raise is an alias for get_or_throw
        self.assertEqual(success_result.get_or_throw(), success_result.get_or_raise())
        with self.assertRaises(ValueError):
            failure_result.get_or_raise()

    def test_throw_on_failure(self):
        """Test the throw_on_failure method"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # Should not raise an exception
        success_result.throw_on_failure()

        # Should raise the stored exception
        with self.assertRaises(ValueError):
            failure_result.throw_on_failure()

        # Test that raise_on_failure is an alias for throw_on_failure
        # Should not raise an exception for success
        success_result.raise_on_failure()

        # Should raise the stored exception for failure
        with self.assertRaises(ValueError):
            failure_result.raise_on_failure()

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

        # on_success with exception in callback should throw
        with self.assertRaises(RuntimeError):
            success_result.on_success(lambda x: exec("raise RuntimeError('on_success error')"))

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

        # on_failure with exception in callback should throw
        with self.assertRaises(RuntimeError):
            failure_result.on_failure(lambda e: exec("raise RuntimeError('on_failure error')"))

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

    def test_map(self):
        """Test the map method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # Map on success should transform the value
        mapped_success = success_result.map(lambda x: x * 2)
        self.assertTrue(mapped_success.is_success)
        self.assertEqual(mapped_success.get_or_null(), 20)

        # Map on failure should return the same failure
        mapped_failure = failure_result.map(lambda x: x * 2)
        self.assertTrue(mapped_failure.is_failure)
        self.assertIsInstance(mapped_failure.exception_or_null(), ValueError)

        # Map with exception in lambda should throw
        with self.assertRaises(ZeroDivisionError):
            success_result.map(lambda x: 1 / 0)

    def test_map_catching(self):
        """Test the map_catching method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # Map catching on success with valid transform
        mapped_success = success_result.map_catching(lambda x: x * 2)
        self.assertTrue(mapped_success.is_success)
        self.assertEqual(mapped_success.get_or_null(), 20)

        # Map catching on success with exception-throwing transform
        mapped_exception = success_result.map_catching(lambda x: 1 / 0)
        self.assertTrue(mapped_exception.is_failure)
        self.assertIsInstance(mapped_exception.exception_or_null(), ZeroDivisionError)

        # Map catching on failure should return the same failure
        mapped_failure = failure_result.map_catching(lambda x: x * 2)
        self.assertTrue(mapped_failure.is_failure)
        self.assertIsInstance(mapped_failure.exception_or_null(), ValueError)

    def test_recover(self):
        """Test the recover method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # Recover on success should return the same result
        recovered_success = success_result.recover(lambda e: 42)
        self.assertTrue(recovered_success.is_success)
        self.assertEqual(recovered_success.get_or_null(), 10)

        # Recover on failure should transform to success
        recovered_failure = failure_result.recover(lambda e: 42)
        self.assertTrue(recovered_failure.is_success)
        self.assertEqual(recovered_failure.get_or_null(), 42)

        # Recover with exception in lambda should throw
        with self.assertRaises(ZeroDivisionError):
            failure_result.recover(lambda e: 1 / 0)

    def test_recover_catching(self):
        """Test the recover_catching method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # Recover catching on success should return the same result
        recovered_success = success_result.recover_catching(lambda e: 42)
        self.assertTrue(recovered_success.is_success)
        self.assertEqual(recovered_success.get_or_null(), 10)

        # Recover catching on failure with valid transform
        recovered_failure = failure_result.recover_catching(lambda e: 42)
        self.assertTrue(recovered_failure.is_success)
        self.assertEqual(recovered_failure.get_or_null(), 42)

        # Recover catching on failure with exception-throwing transform
        recovered_exception = failure_result.recover_catching(lambda e: 1 / 0)
        self.assertTrue(recovered_exception.is_failure)
        self.assertIsInstance(recovered_exception.exception_or_null(), ZeroDivisionError)

    def test_fold(self):
        """Test the fold method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # Fold on success should call onSuccess
        success_value = success_result.fold(
            on_success=lambda x: f"Success: {x}",
            on_failure=lambda e: f"Failure: {e}"
        )
        self.assertEqual(success_value, "Success: 10")

        # Fold on failure should call onFailure
        failure_value = failure_result.fold(
            on_success=lambda x: f"Success: {x}",
            on_failure=lambda e: f"Failure: {e}"
        )
        self.assertEqual(failure_value, "Failure: test error")

        # Fold with exception in onSuccess lambda should throw
        with self.assertRaises(ZeroDivisionError):
            success_result.fold(
                on_success=lambda x: 1 / 0,
                on_failure=lambda e: 0.0  # Same type as 1 / 0 would return (float)
            )

        # Fold with exception in onFailure lambda should throw
        with self.assertRaises(RuntimeError):
            failure_result.fold(
                on_success=lambda x: None,  # Same type as exec() returns (None)
                on_failure=lambda e: exec("raise RuntimeError('fold error')")
            )

    def test_get_or_else(self):
        """Test the get_or_else method"""
        success_result = Result.success(10)
        failure_result = Result.failure(ValueError("test error"))

        # get_or_else on success should return the value
        success_value = success_result.get_or_else(lambda e: 42)
        self.assertEqual(success_value, 10)

        # get_or_else on failure should call the callback
        failure_value = failure_result.get_or_else(lambda e: 42)
        self.assertEqual(failure_value, 42)

        # get_or_else on failure can use the exception
        failure_msg = failure_result.get_or_else(lambda e: f"Error occurred: {e}")
        self.assertEqual(failure_msg, "Error occurred: test error")

        # get_or_else with exception in lambda should throw
        with self.assertRaises(ZeroDivisionError):
            failure_result.get_or_else(lambda e: 1 / 0)

    def test_get_or_null_and_exception_or_null(self):
        """Test get_or_null and exception_or_null main methods"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # Test get_or_null
        self.assertEqual(success_result.get_or_null(), "test value")
        self.assertIsNone(failure_result.get_or_null())

        # Test exception_or_null
        self.assertIsNone(success_result.exception_or_null())
        self.assertIsInstance(failure_result.exception_or_null(), ValueError)

        # Test that get_or_none is an alias for get_or_null
        self.assertEqual(success_result.get_or_null(), success_result.get_or_none())
        self.assertEqual(failure_result.get_or_null(), failure_result.get_or_none())

        # Test that exception_or_none is an alias for exception_or_null
        self.assertEqual(success_result.exception_or_null(), success_result.exception_or_none())
        self.assertEqual(failure_result.exception_or_null(), failure_result.exception_or_none())

    def test_str_and_repr(self):
        """Test __str__ and __repr__ methods"""
        success_result = Result.success("test value")
        failure_result = Result.failure(ValueError("test error"))

        # Test __str__
        self.assertEqual(str(success_result), "Success(test value)")
        self.assertEqual(str(failure_result), "Failure(test error)")

        # Test __repr__
        self.assertEqual(repr(success_result), "Result.success('test value')")
        self.assertEqual(repr(failure_result), "Result.failure(ValueError('test error'))")

    def test_equality(self):
        """Test __eq__ and __ne__ methods"""
        # Success results with same value should be equal
        result1 = Result.success(42)
        result2 = Result.success(42)
        result3 = Result.success(43)
        self.assertEqual(result1, result2)
        self.assertNotEqual(result1, result3)

        # Failure results with same exception should be equal
        error1 = Result.failure(ValueError("error"))
        error2 = Result.failure(ValueError("error"))
        error3 = Result.failure(ValueError("different"))
        error4 = Result.failure(TypeError("error"))
        self.assertEqual(error1, error2)
        self.assertNotEqual(error1, error3)
        self.assertNotEqual(error1, error4)

        # Success and failure should never be equal
        self.assertNotEqual(Result.success(42), Result.failure(ValueError("error")))

        # Result should not be equal to non-Result
        self.assertNotEqual(Result.success(42), 42)
        self.assertNotEqual(Result.success(42), "42")

    def test_hash(self):
        """Test __hash__ method"""
        # Same success results should have same hash
        result1 = Result.success(42)
        result2 = Result.success(42)
        self.assertEqual(hash(result1), hash(result2))

        # Same failure results should have same hash
        error1 = Result.failure(ValueError("error"))
        error2 = Result.failure(ValueError("error"))
        self.assertEqual(hash(error1), hash(error2))

        # Results can be used in sets
        result_set = {Result.success(1), Result.success(2), Result.success(1)}
        self.assertEqual(len(result_set), 2)

        # Results can be used as dict keys
        result_dict = {Result.success(1): "one", Result.failure(ValueError("e")): "error"}
        self.assertEqual(result_dict[Result.success(1)], "one")
        self.assertEqual(result_dict[Result.failure(ValueError("e"))], "error")
