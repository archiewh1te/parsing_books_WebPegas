import logging
import time
from functools import wraps


def retry_on_exception(exceptions, max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    logging.error(f"Exception {e} occurred. Retrying in 1 second... Attempt {attempts}/{max_attempts}")
                    time.sleep(1)
            try:
                raise
            except exceptions as e:
                logging.error(f"Max retry limit reached. Exception {e} could not be handled after {attempts} attempts.")
                raise

        return wrapper

    return decorator


@retry_on_exception((RuntimeError, ValueError), 3)
def example_function(a, b):
    if a > b:
        return a / b
    else:
        raise ValueError("Invalid input")


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    result = example_function(2, 0)
    logging.info(f"Result: {result}")
except Exception as e:
    logging.error(f"An exception occurred: {e}")
