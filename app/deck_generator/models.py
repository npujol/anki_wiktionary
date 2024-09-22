from typing import Any

import genanki
from anki.collection import Collection
from anki.collection_pb2 import OpChangesWithId
from anki.models import ModelManager
from pydantic import BaseModel

from .helpers import generate_random_id

BASIC_MODEL_FRONT_TEMPLATE = """
<div id="rubric">GeneratedBasicModel</div>
<div id="front">
    {{front}}
</div>
"""

BASIC_MODEL_BACK_TEMPLATE = """
<div id="rubric">GeneratedBasicModel</div>
<div id="front">
{{front}}
</div>
<hr id="answer">
<div id="back">
{{back}}
</div>
"""

BASIC_MODEL_CSS = """
.card {
font-family: arial;
font-size:200%;
text-align: center;
color: Black;
background-color:black;
}

#rubric {
text-align: left;
padding: 4px;
padding-left: 10px;
padding-right: 10px;
margin-bottom: 10px;
background: #1d6695;
color: white;
font-weight: 500;
}

#front {
font-family: Arial;
font-size: 40px;
color:#FF80DD;
}

#back {
font-family: Arial;
font-size: 35px;
}
"""


class BasicModel(BaseModel):
    name: str = "GeneratedBasicModel"

    def anki_fields(self) -> list[dict[str, str]]:
        return [
            {"name": "front"},
            {"name": "back"},
        ]

    def anki_templates(self) -> list[dict[str, str]]:
        return [
            {
                "name": self.name,
                "qfmt": BASIC_MODEL_FRONT_TEMPLATE,
                "afmt": BASIC_MODEL_BACK_TEMPLATE,
            },
        ]

    def anki_ccs(self) -> str:
        return BASIC_MODEL_CSS

    def __str__(self) -> str:
        return self.name

    def to_genanki_model(self) -> genanki.Model:
        return genanki.Model(
            model_id=generate_random_id(),
            name=self.name,
            fields=self.anki_fields(),
            templates=self.anki_templates(),
            css=self.anki_ccs(),
        )

    def to_anki_model(self, col: Collection, model_name: str) -> dict[str, Any]:
        mm: ModelManager = col.models

        custom_model: dict[str, Any] = mm.new(model_name)

        mm.add_field(notetype=custom_model, field=mm.new_field(name="front"))
        mm.add_field(notetype=custom_model, field=mm.new_field(name="back"))

        custom_model["tmpls"] = [
            {
                "name": self.name,
                "qfmt": BASIC_MODEL_FRONT_TEMPLATE,
                "afmt": BASIC_MODEL_BACK_TEMPLATE,
                "css": BASIC_MODEL_CSS,
            }
        ]

        mm.add_dict(notetype=custom_model)
        return custom_model


class BasicModelContent(BaseModel):
    front: str
    back: str
    type: BasicModel = BasicModel()

    def __str__(self) -> str:
        return f"Front: {self.front}, Back: {self.back}"
