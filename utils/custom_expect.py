from typing import Any

from utils.apilogger import APILogger


class Expect:
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


_api_logger: APILogger | None = None


def set_custom_api_logger(logger: APILogger):
    global _api_logger
    _api_logger = logger


def expect(actual: Any) -> Expect:
    """Factory function to create Expect objects"""
    return Expect(actual, _api_logger)
