import datetime
import time
from config import show_elapsed_time


def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        val = func(*args, **kwargs)
        elapsed_time_float = datetime.datetime.now() - start_time
        seconds = elapsed_time_float.total_seconds()
        if seconds < 0.3:
            time.sleep(0.3 - seconds)
        if show_elapsed_time:
            print(f'[INFO] Elapsed time: {elapsed_time_float}')
        return val
    return wrapper
