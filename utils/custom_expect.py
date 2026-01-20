from typing import Any

from utils.apilogger import APILogger
from utils.schema_validator import validate_schema


class Expect:
    """
    Custom assertion class for API testing with logging capabilities.

    Provides a fluent interface for making assertions on API responses and logging recent API activity.

    Can be extended by adding should_not_* methods for negated assertions.
    Can be extended by adding should_less_then_or_equal and other custom assertions.
    """

    def __init__(self, actual: Any, logger: APILogger | None = None):
        self.actual = actual
        self.logger = logger

    def should_equal(self, expected: Any):
        try:
            assert self.actual == expected
        except AssertionError as e:
            logs = self.logger.get_recent_logs() if self.logger else "No logs available"
            raise AssertionError(
                f"\nExpected: {expected}\n"
                f"Actual: {self.actual}\n\n"
                f"Recent API activity:\n\n{logs}"
            )
        return self

    def should_match_schema(self, directory_name: str, file_name: str):
        """
        Validates the actual value against a JSON schema.

        Args:
            directory_name: The subdirectory name under response-schemas
            file_name: The schema file name (without _schema.json suffix)
        """
        try:
            validate_schema(directory_name, file_name, self.actual)
        except AssertionError as e:
            logs = self.logger.get_recent_logs() if self.logger else "No logs available"
            raise AssertionError(
                f"\n{str(e)}\n\n"
                f"Recent API activity:\n\n{logs}"
            )
        return self

_api_logger: APILogger | None = None


def set_custom_api_logger(logger: APILogger):
    global _api_logger
    _api_logger = logger


def expect(actual: Any) -> Expect:
    """Factory function to create Expect objects"""
    return Expect(actual, _api_logger)
