import traceback
import functools
from datetime import timedelta, date


def check_test(func):
    @functools.wraps(func)  # This preserves the original function's name and other metadata
    def wrapper(*args, **kwargs):
        try:
            print(f"Running Test <{func.__name__}>...")
            func(*args, **kwargs)
            print(f"{func.__name__} - PASSED")
            return True
        except AssertionError:
            print(f"{func.__name__} - FAIL")
            print(traceback.format_exc())
        except Exception:
            print(f"{func.__name__} - FAIL - Exception")
            print(traceback.format_exc())

        return False
    return wrapper


def get_dates(offset: int = 0, delta: int = 0):
    start_date = date.today() + timedelta(days=offset)
    end_date = start_date + timedelta(days=delta)
    return str(start_date), str(end_date)
