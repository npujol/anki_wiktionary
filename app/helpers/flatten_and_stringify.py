from typing import Any, Union


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
