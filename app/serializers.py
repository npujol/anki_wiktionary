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
    audio: list[AudioItem]
    video: list[VideoItem]
    picture: list[PictureItem]


class Params(BaseModel):
    notes: list[Note]


class Model(BaseModel):
    action: str
    version: int
    params: Params
