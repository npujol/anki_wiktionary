from typing import Any

import pytest

from app.helpers.flatten_and_stringify import clean_request_body


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    return {
        "ignore_localhost": True,
        "before_record_request": clean_request_body(),
    }
