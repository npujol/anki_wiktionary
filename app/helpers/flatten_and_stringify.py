from typing import Union


def flatten_and_stringify(
    content: Union[str, list, None], separator: str = "\n"
) -> str:
    if isinstance(content, str):
        return content
    stack = [content]
    flat_list = []

    while stack:
        current = stack.pop()
        if isinstance(current, str):
            flat_list.append(current)
        elif isinstance(current, list):
            stack.extend(current[::-1])
    return separator.join(flat_list) if flat_list else ""
