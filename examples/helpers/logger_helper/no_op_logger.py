"""
This module contains the definition of no-op logger.
Its `NoOpLogger()` instance can be passed as a default parameter to a function
or method with logging and replaced with a real logger by calling.
"""


class NoOpLogger:
    """The no-op logger does nothing."""

    def write(self, *args, **kwargs):
        pass

    def debug(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def warn(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

    def critical(self, *args, **kwargs):
        pass

    def console(self, *args, **kwargs):
        pass

    def trace(self, *args, **kwargs):
        pass
