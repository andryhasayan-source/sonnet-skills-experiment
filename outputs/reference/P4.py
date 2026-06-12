import functools
import time

def retry(times=3, delay=0.1, exceptions=(Exception,)):
    if times < 1:
        raise ValueError("times must be >= 1")
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last = e
                    if attempt < times - 1 and delay:
                        time.sleep(delay)
            raise last
        return wrapper
    return decorator
