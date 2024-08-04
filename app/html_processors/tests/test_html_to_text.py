import pytest

from app.html_processors import extract_ordered_text


@pytest.mark.parametrize(
    "raw_html,expected_text",
    [
        (
            "<h1>Test Header 1</h1><p>Test paragraph 1</p>",
            "\n# Test Header 1\n\nTest paragraph 1\n",
        ),
        (
            "<h2>Test Header 2</h2><p>Test paragraph 2</p>",
            "\n## Test Header 2\n\nTest paragraph 2\n",
        ),
        (
            "<h3>Test Header 3</h3><p>Test paragraph 3</p>",
            "\n### Test Header 3\n\nTest paragraph 3\n",
        ),
        (
            "<ul><li>Test list item 1</li><li>Test list item 2</li></ul>",
            "* Test list item 1\n* Test list item 2\n",
        ),
    ],
)
def test_extract_ordered_text(raw_html: str, expected_text: str) -> None:
    """Test extract_ordered_text function."""
    result: str = extract_ordered_text(raw_html=raw_html)
    assert (
        result == expected_text
    ), f"Result: {result}, Expected: {expected_text} should be equal."
