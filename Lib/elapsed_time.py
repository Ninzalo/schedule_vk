import datetime


def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        val = func(*args, **kwargs)
        print(f'[INFO] Elapsed time: {datetime.datetime.now() - start_time}')
        return val
    return wrapper
