import inspect
from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest

from .errors import InvalidTokenError


def is_method(function: Callable) -> bool:
    spec = inspect.signature(function)
    return spec.parameters.get("self")


def require_jwt(func: Callable[[HttpRequest], Any] | Callable[[Any, HttpRequest], Any]):
    @wraps(func)
    def _inner_for_func(request: HttpRequest, *args, **kwargs):
        if not request.jwt_user_id:
            raise InvalidTokenError
        return func(request, *args, **kwargs)

    @wraps(func)
    def _inner_for_class(_instance, request: HttpRequest, *args, **kwargs):
        if not request.jwt_user_id:
            raise InvalidTokenError
        return func(_instance, request, *args, **kwargs)

    return _inner_for_class if is_method(func) else _inner_for_func
