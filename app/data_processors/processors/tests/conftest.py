import pytest

from app.serializers import CustomNote


@pytest.fixture()  # type: ignore
def initial_note() -> CustomNote:
    return CustomNote(
        deckName="Test",
        modelName="Basic_",
        tags=[],
        audio=[],
        video=[],
        picture=[],
    )
