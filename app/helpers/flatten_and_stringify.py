import re
from typing import Any, Callable, Union

from requests import Request


def flatten_and_stringify(content: Union[str, list[Any]], separator: str = "\n") -> str:
    if isinstance(content, str):
        return content
    stack: list[Any] = [content]
    flat_list: list[str] = []

    while stack:
        current: Any = stack.pop()
        if isinstance(current, str):
            flat_list.append(current)
        elif isinstance(current, list):
            stack.extend(current[::-1])  # type: ignore
    return separator.join(flat_list) if flat_list else ""


def clean_request_body() -> Callable[..., Any]:
    def before_record_request(request: Request) -> Request:
        request.body = b"{}"  # type: ignore
        current_uri: str = request.uri  # type: ignore
        request.uri = re.sub(pattern=r"\d", repl="1", string=current_uri)  # type: ignore
        return request

    return before_record_request
