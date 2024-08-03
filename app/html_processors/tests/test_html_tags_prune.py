import pytest
from bs4 import BeautifulSoup

from app.html_processors import prune_html_tags


@pytest.mark.parametrize(
    "test_html, expected_html",
    [
        (
            "<h1>Hello</h1><script>alert('hello')</script>",
            "<h1>Hello</h1>",
        ),
        (
            "<h1>Hello</h1><div><p>World</p></div>",
            "<h1>Hello</h1><div><p>World</p></div>",
        ),
        (
            "<h1>Hello</h1><div><p>World</p></div><img src='hello'/>",
            "<h1>Hello</h1><div><p>World</p></div>",
        ),
        (
            (
                "<h1>Hello</h1><div><p>World</p></div><img src='hello'/><button>Click"
                "</button>"
            ),
            "<h1>Hello</h1><div><p>World</p></div>",
        ),
    ],
)
def test_prune_html_tags(test_html, expected_html) -> None:
    """Test that specified tags are removed from the HTML."""
    html = BeautifulSoup(markup=test_html, features="html.parser")
    expected_html = BeautifulSoup(markup=expected_html, features="html.parser")

    result_html = prune_html_tags(html=html)

    assert (
        result_html == expected_html
    ), f"Result: {result_html}, Expected: {expected_html} should be equal."
