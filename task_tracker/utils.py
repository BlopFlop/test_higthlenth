from functools import wraps

from pydantic_core import ValidationError


def except_control(value_exc_msg: str, validate_err_msg: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except ValueError:
                print(value_exc_msg)
            except ValidationError:
                print(validate_err_msg)
            return result

        return wrapper

    return decorator
