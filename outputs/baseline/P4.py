import time
import functools


def retry(times: int = 3, delay: float = 0.1, exceptions: tuple = (Exception,)):
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < times - 1:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator