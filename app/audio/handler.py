import logging
from pathlib import Path

from gtts import gTTS  # type: ignore

from app.helpers import to_valid_filename
from app.private_config import working_path


class AudioHandler:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name=__name__)

        self.audios_path: Path = working_path / "audios"
        self.audios_path.mkdir(parents=True, exist_ok=True)

    async def generate_audio(self, text: str, language_code: str = "de") -> Path:
        """
        Asynchronously generates audio for a given text.

        Args:
            text (str): The text to generate audio for.
            language_code (str, optional): The language code to use. Defaults to "de".

        Returns:
            Path: The path to the generated audio file.
        """
        tts = gTTS(text=text, lang=language_code)  # type: ignore

        path: Path = self.audios_path / f"{to_valid_filename(text)}.mp3"
        tts.save(savefile=path)  # type: ignore

        return path
