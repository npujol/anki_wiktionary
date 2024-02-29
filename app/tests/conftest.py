import pytest

from app.connector import AnkiConnector
from app.serializers import Note


@pytest.fixture()
def note_data():
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
def add_note_request(note_data):
    return {
        "action": "addNotes",
        "version": 6,
        "params": {"notes": [note_data]},
    }


@pytest.fixture
def note_obj(note_data):
    return Note.model_validate(
        note_data,
        from_attributes=True,
        strict=False,
    )


@pytest.fixture()
def add_note_result():
    {"result": [1496198395707, None], "error": None}


@pytest.fixture()
def anki_connector():
    return AnkiConnector()
