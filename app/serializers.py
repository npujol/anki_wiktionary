from typing import Any, Optional

from deep_translator import GoogleTranslator
from pydantic import BaseModel, Field, model_validator


class Fields(BaseModel):
    front: str = Field(..., alias="Front")
    back: str = Field(..., alias="Back")


class AudioItem(BaseModel):
    url: str
    filename: str
    skip_hash: str = Field(..., alias="skipHash")
    fields: list[str]


class VideoItem(BaseModel):
    url: str
    filename: str
    skip_hash: str = Field(..., alias="skipHash")
    fields: list[str]


class PictureItem(BaseModel):
    url: str
    filename: str
    skip_hash: str = Field(..., alias="skipHash")
    fields: list[str]


class Note(BaseModel):
    deck_name: str = Field(..., alias="deckName")
    note_model_name: str = Field(..., alias="modelName")
    fields: Fields
    tags: list[str]
    audio: list[AudioItem] = []
    video: list[VideoItem] = []
    picture: list[PictureItem] = []
    # options: dict = {"allowDuplicate": False}


class Params(BaseModel):
    notes: list[Note]


class Model(BaseModel):
    action: str
    version: int
    params: Params


class CustomFields(BaseModel):
    full_word: str
    plural: Optional[str] = None
    characteristics: Optional[str] = None
    ipa: Optional[str] = None
    audio: Optional[list[AudioItem]] = None
    meaning: Optional[str] = None
    meaning_spanish: Optional[str] = None
    example1: Optional[str] = None
    example1e: Optional[str] = None
    example2: Optional[str] = None
    example2e: Optional[str] = None

    @model_validator(mode="before")
    def validate_missing_translations(cls, values: Any) -> Any:
        handler = GoogleTranslator(source="de", target="es")
        to_translate_map = {
            "meaning": "meaning_spanish",
            "example1": "example1e",
            "example2": "example2e",
        }
        for original, to_generate in to_translate_map.items():
            original_value = values.get(original, None)
            if not values.get(to_generate, None) and original_value:
                trans_result = handler.translate(
                    original_value,
                )
                values[to_generate] = trans_result if trans_result else ""
        return values


class CustomNote(Note):
    # overrides symbol of same name in class "Note"
    fields: CustomFields  # type: ignore

    def pretty_print(self) -> str:
        msg = (
            f"full_word:\n    {self.fields.full_word}\n\n"
            + f"plural:\n    {self.fields.plural}\n\n"
            + f"characteristics:\n    {self.fields.characteristics}\n\n"
            + f"ipa:\n    {self.fields.ipa}\n\n"
            + f"audio:\n    {self.fields.audio}\n\n"
            + f"meaning:\n    {self.fields.meaning}\n\n"
            + f"meaning_spanish:\n    {self.fields.meaning_spanish}\n\n"
            + f"example1:\n    {self.fields.example1}\n\n"
            + f"example1e:\n    {self.fields.example1e}\n\n"
            + f"example2:\n    {self.fields.example2}\n\n"
            + f"example2e:\n    {self.fields.example2e}\n"
        )
        return msg
