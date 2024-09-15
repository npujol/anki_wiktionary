from pathlib import Path

import pytest

from app.audio import AudioHandler


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_generate_audio(audio_handler: AudioHandler) -> None:
    """
    Tests the generate_audio function.
    """
    text: str = "Hello, world!"
    path: Path = await audio_handler.generate_audio(text=text)

    assert path.exists(), "The audio file was not generated."
    assert path.suffix == ".mp3", "The file is not an mp3."

    path.unlink()
