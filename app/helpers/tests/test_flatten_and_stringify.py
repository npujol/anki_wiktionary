import pytest

from app.helpers import flatten_and_stringify


@pytest.mark.parametrize(
    "content, separator, expected_result",
    [
        (["a", "b"], " ", "a b"),
        (["a", ["b", "c"]], " ", "a b c"),
        (["a", ["b", ["c", "d"]]], " ", "a b c d"),
        (["a", ["b", ["c", "d"]]], "\n", "a\nb\nc\nd"),
        (None, " ", ""),
        ([""], " ", ""),
        (["a", []], " ", "a"),
        (["a", ["b", []]], " ", "a b"),
    ],
)
def test_flatten_and_stringify(content, separator, expected_result) -> None:
    """Test the flatten_and_stringify function."""
    result = flatten_and_stringify(content=content, separator=separator)
    assert (
        result == expected_result
    ), f"Result: {result}, Expected: {expected_result} should be equal."
