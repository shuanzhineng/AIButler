import json

from common.base_pydantic import CustomBaseModel, CreatorOut
from pydantic import field_validator
from apps.data.models.db import LabelTask, LabelTaskSample
from tortoise.contrib.pydantic.creator import pydantic_model_creator

# ---------------------标注任务model------------------------
_LabelTaskOut = pydantic_model_creator(LabelTask, name="_LabelTaskOut")
_LabelTaskSampleOut = pydantic_model_creator(LabelTaskSample, name="_LabelTaskSampleOut")


class LabelTaskOut(_LabelTaskOut, CustomBaseModel):  # type: ignore
    creator: CreatorOut | None = None


class LabelTaskSampleOut(_LabelTaskSampleOut, CustomBaseModel):  # type: ignore
    @field_validator(
        "data",
    )
    @classmethod
    def change_genre(cls, v):
        return json.dumps(v, ensure_ascii=False)
