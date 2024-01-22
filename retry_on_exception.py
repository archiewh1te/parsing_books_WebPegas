import logging
import time
from functools import wraps


def retry_on_exception(exceptions, max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logging.error(
                        f"Exception {e} occurred. Retrying in 1 second... Attempt {attempt + 1}/{max_attempts}")
                    time.sleep(1)
            if last_exception is not None:
                logging.error(f"Max retry limit reached. Last exception: {last_exception}")
                raise last_exception

        return wrapper

    return decorator


@retry_on_exception((ZeroDivisionError, KeyError), 3)
def risky_operation(x, y):
    if x > y:
        return x / y
    else:
        raise KeyError("Invalid input")


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    result = risky_operation(10, 0)
    logging.info(f"Result: {result}")
except Exception as e:
    logging.error(f"An exception occurred: {e}")
