from typing import Any

import pytest

from app.serializers import CustomNote


@pytest.fixture()
def custom_note_data() -> dict[str, Any]:
    return {
        "deckName": "Test",
        "modelName": "Basic_",
        "fields": {
            "full_word": "content1",
            "plural": "content1",
            "characteristics": "content1",
            "ipa": "content1",
            "meaning": "content1",
            "meaning_spanish": "content1",
            "example1": "content1",
            "example1e": "content1",
            "example2": "content1",
            "example2e": "content1",
        },
        "tags": ["test"],
        "audio": [
            {
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": ["audio"],
            }
        ],
        "options": {"allowDuplicate": True},
    }


@pytest.fixture()  # type: ignore
def add_custom_note_request(custom_note_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "action": "addNotes",
        "version": 6,
        "params": {"notes": [custom_note_data]},
    }


@pytest.fixture
def custom_note_obj(custom_note_data: dict[str, Any]) -> CustomNote:
    return CustomNote.model_validate(
        obj=custom_note_data,
        from_attributes=True,
        strict=False,
    )
