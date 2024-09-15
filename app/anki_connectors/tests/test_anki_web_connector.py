import pytest

from app.anki_connectors import AnkiWebConnector
from app.serializers import CustomNote


@pytest.mark.vcr()
def test_start(anki_web_connector: AnkiWebConnector) -> None:
    anki_web_connector.start()
    assert anki_web_connector.driver is not None
    # Check if the login was successful by inspecting the driver's current URL
    assert "login" in anki_web_connector.driver.current_url
    assert anki_web_connector.driver.title == "Login - AnkiWeb"
    # anki_web_connector.close()


@pytest.mark.vcr()
def test_send_card_success(
    anki_web_connector: AnkiWebConnector,
    custom_note_obj: CustomNote,
) -> None:
    anki_web_connector.start()

    tags: list[str] = ["tag1", "tag2"]
    card_type = "Basic_"

    result: bool = anki_web_connector.send_card(
        custom_note=custom_note_obj, tags=tags, card_type=card_type
    )
    assert result is True, "Card was not sent successfully"
    assert anki_web_connector.driver.title == "Add - AnkiWeb"

    # anki_web_connector.close()
