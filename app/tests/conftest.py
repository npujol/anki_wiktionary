import pytest


@pytest.fixture
def add_note_request():
    return {
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": [
                {
                    "deckName": "Default",
                    "modelName": "Basic",
                    "fields": {"Front": "front content", "Back": "back content"},
                    "tags": ["yomichan"],
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
                }
            ]
        },
    }


@pytest.fixture()
def add_note_result():
    {"result": [1496198395707, None], "error": None}
