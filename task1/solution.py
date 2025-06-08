from typing import Callable
import functools
import inspect

def strict(func: Callable) -> Callable:

    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        """Проходимся по аннотациям и проверяем параметры на соответствие."""

        errors = {}
        sig = inspect.signature(func)
        bound_params = sig.bind(*args, **kwargs)
        bound_params.apply_defaults() # Если будут значения по умолчанию

        for name, param in list(sig.parameters.items()):
            param_value = bound_params.arguments.get(name)
            expected_type = param.annotation

            if expected_type is inspect._empty:
                continue

            if not isinstance(param_value, expected_type):
                errors.setdefault(name, f'Expected type is {expected_type}, '
                                        f'got {type(param_value)} instead')
        if errors:
            raise TypeError(errors)

        return func(*args, **kwargs)

    return wrap_func


@strict
def sum_two(a: int, b: int) -> int:
    """Сумма двух чисел"""

    return a + b


if __name__ == '__main__':
    print(sum_two(1, 3))
