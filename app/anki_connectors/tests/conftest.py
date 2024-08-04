import re
from typing import Any, Callable

import pytest
from requests import Request

from app.anki_connectors.anki_local_connector import AnkiLocalConnector
from app.anki_connectors.anki_web_connector import AnkiWebConnector
from app.serializers import CustomNote, Note


def clean_request_body() -> Callable[..., Any]:
    def before_record_request(request: Request) -> Request:
        request.body = b"{}"  # type: ignore
        current_uri: str = request.uri  # type: ignore
        request.uri = re.sub(pattern=r"\d", repl="1", string=current_uri)  # type: ignore
        return request

    return before_record_request


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Callable[..., Any]]:
    return {
        "before_record_request": clean_request_body(),
    }


@pytest.fixture()
def note_data() -> dict[str, Any]:
    return {
        "deckName": "Test",
        "modelName": "Basic",
        "fields": {"Front": "front content1", "Back": "back content1"},
        "tags": ["test"],
        "audio": [
            {
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": ["Front"],
            }
        ],
        "video": [
            {
                "url": "https://cdn.videvo.net/videvo_files/video/free/2015-06/small_watermarked/Contador_Glam_preview.mp4",
                "filename": "countdown.mp4",
                "skipHash": "4117e8aab0d37534d9c8eac362388bbe",
                "fields": ["Back"],
            }
        ],
        "picture": [
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                "filename": "black_cat.jpg",
                "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                "fields": ["Back"],
            }
        ],
        "options": {"allowDuplicate": True},
    }


@pytest.fixture
def add_note_request(note_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "action": "addNotes",
        "version": 6,
        "params": {"notes": [note_data]},
    }


@pytest.fixture
def note_obj(note_data: dict[str, Any]) -> Note:
    return Note.model_validate(
        obj=note_data,
        from_attributes=True,
        strict=False,
    )


@pytest.fixture()
def anki_local_connector() -> AnkiLocalConnector:
    return AnkiLocalConnector()


@pytest.fixture(scope="function")
def anki_web_connector() -> AnkiWebConnector:
    return AnkiWebConnector(username="username", password="password")


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


@pytest.fixture
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
