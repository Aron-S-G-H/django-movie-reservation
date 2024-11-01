from typing import Sequence, Any
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.fields import empty
from functools import wraps


def custom_decorator(
        request: Any = empty,
        responses: Any = empty,
        methods: Sequence[str] | None = None,
        url_path: str | None = None,
        url_name: str | None = None,
        summary: str | None = None,
        detail: bool = False,
        description: str | None = None,
        examples: Sequence[OpenApiExample] | None = None,
        parameters: Sequence[OpenApiParameter] | None = None
):
    def decorator(func):
        @extend_schema(
            request=request,
            responses=responses,
            methods=methods,
            summary=summary,
            description=description,
            examples=examples,
            parameters=parameters,
        )
        @action(methods=methods, url_path=url_path, detail=detail, url_name=url_name)
        @wraps(func)  # Ensures the wrapper keeps the original function's metadata
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
