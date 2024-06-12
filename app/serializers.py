import logging
from typing import Any, Callable, Optional, Self

from deep_translator import GoogleTranslator
from pydantic import BaseModel, Field, ValidationError, computed_field, model_validator

logger = logging.getLogger(name=__name__)


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


class BasicFields(BaseModel):  # that needs to be updated
    Front: str = Field(
        default=...,
        description="This field contains the input word to be used in the generated content.",
    )
    Back: str = Field(
        default=...,
        description="This field contains html content with the information of the word.",
    )


# NOTE: To handle multiple card types in the future, this is the only element
# that needs to be updated
class CustomFields(BaseModel):
    full_word: str = Field(
        default=...,
        description="This field contains the input word to be used in the generated content.",
    )
    plural: Optional[str] = Field(
        default=None,
        description="This field contains the plural form of the word.",
    )
    characteristics: Optional[str] = Field(
        default=None,
        description="This field contains specific grammatical characteristics of the word.",
    )
    ipa: Optional[str] = Field(
        default=None,
        description="This field contains the IPA transcription of the word.",
    )
    audio: Optional[list[AudioItem]] = Field(
        default=None,
        description="This field contains the audio files associated with the word. In the generation process this field will be ignored.",
    )
    meaning: Optional[str] = Field(
        default=None,
        description="This field contains the meaning of the word. This field should include the different meanings of the word, including the slangs. Start each meaning on a new line.",
    )
    meaning_spanish: Optional[str] = Field(
        default=None,
        description="This field contains the meaning of the word in Spanish. This field should be ignores in the generation process.",
    )
    example1: Optional[str] = Field(
        default=None,
        description="This field contains one example sentence using the word.",
    )
    example1e: Optional[str] = Field(
        default=None,
        description="This field contains the meaning of the word in Spanish. This field should be ignores in the generation process.",
    )
    example2: Optional[str] = Field(
        default=None,
        description="This field contains one example sentence using the word. The example sentence should be different from the first example sentence in the example1 field.",
    )
    example2e: Optional[str] = Field(
        default=None,
        description="This field contains the meaning of the word in Spanish. This field should be ignores in the generation process.",
    )

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
                    text=original_value,
                )
                values[to_generate] = trans_result if trans_result else ""
        return values

    @classmethod
    def model_json_schema_to_generate_fields(cls) -> dict[str, Any]:
        fields_to_generate = [
            "plural",
            "characteristics",
            "ipa",
            "meaning",
            "example1",
            "example2",
        ]
        schema = cls.model_json_schema().get("properties", {})
        return {key: schema[key] for key in schema.keys() if key in fields_to_generate}


class CustomNote(Note):
    # overrides symbol of same name in class "Note"
    fields: CustomFields | BasicFields | None = None

    @computed_field(return_type=str)
    def word(cls) -> str:
        word = "default"
        if cls.fields is not None and isinstance(cls.fields, CustomFields):
            word = cls.fields.full_word
        if cls.fields is not None and isinstance(cls.fields, BasicFields):
            word = cls.fields.Front
        return word

    @computed_field(return_type=str)
    def card_type(cls) -> str:
        card_type = "Basic"
        if cls.fields is not None and isinstance(cls.fields, CustomFields):
            card_type = "Basic_"
        if cls.fields is not None and isinstance(cls.fields, BasicFields):
            card_type = "Basic"
        return card_type

    def pretty_print(self) -> str:
        msg = "No fields found"
        if not self.fields:
            return msg
        if isinstance(self.fields, CustomFields):
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
        if isinstance(self.fields, BasicFields):
            # TODO Check how can I reduce the size of this message
            msg = (
                f"Front:\n    {self.fields.Front}\n\n"
                + f"Back:\n    {self.fields.Back[:200]}\n\n"
            )

        return msg

    def import_from_content(
        self, content: dict[str, Any], fields_class: Callable
    ) -> Self | None:
        try:
            self.fields = fields_class(  # type: ignore
                **{k: v for k, v in content.items() if k in fields_class.model_fields}  # type: ignore
            )
            return self
        except ValidationError as e:
            logger.exception(msg=f"Failed to import note from content: {e}")
            return None
