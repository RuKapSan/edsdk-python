from edsdk import EdsError
from time import sleep
from logging import debug


def safe_api_access(func):
    """Decorator that retries a api call 5 times if it raises an EdsError"""
    def wrapper(*args, **kwargs):
        err = None
        for i in range(5):
            try:
                return func(*args, **kwargs)
            except EdsError as e:
                err = e
                debug(f"Error {e} while executing {func.__name__}, retrying in 1 second, attempt {i+1}/5")
                sleep(1)
        raise EdsError(f"Error: {err} while executing {func.__name__}, retry limit reached")
    return wrapper