from typing import Any
import pytest

from app.main import generate_notes


@pytest.mark.vcr()
def test_generate_notes(snapshot: Any):
    result = generate_notes(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result
