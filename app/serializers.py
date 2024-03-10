from typing import Optional
from pydantic import BaseModel, Field


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
    model_name: str = Field(..., alias="modelName")
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


class CustomNote(Note):
    fields: CustomFields

    def pretty_print(self) -> str:
        msg = (
            f"full_word: {self.fields.full_word}\nplural: {self.fields.plural}"
            + f"\ncharacteristics: {self.fields.characteristics}\nipa: "
            + f"{self.fields.ipa}\naudio: {self.fields.audio}\nmeaning: "
            + f"{self.fields.meaning}\nmeaning_spanish: {self.fields.meaning_spanish}\n"
            + f"example1: {self.fields.example1}\nexample1e: "
            + f"{self.fields.example1e}\nexample2: {self.fields.example2}\nexample2e: "
            + f"{self.fields.example2e}"
        )
        return msg
