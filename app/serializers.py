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
