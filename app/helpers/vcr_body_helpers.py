import re
from typing import Any, Callable

from requests import Request


def clean_request_body() -> Callable[..., Any]:
    def before_record_request(request: Request) -> Request:
        request.body = b"{}"  # type: ignore
        current_uri: str = request.uri  # type: ignore
        request.uri = re.sub(pattern=r"\d", repl="1", string=current_uri)  # type: ignore
        return request

    return before_record_request
