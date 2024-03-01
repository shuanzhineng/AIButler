from common.base_pydantic import CustomBaseModel
from pydantic import Field

from typing import Any
from common.enums import MediaTypeEnum, LabelTaskSampleStateEnum


class LabelTaskIn(CustomBaseModel):
    name: str = Field(min_length=1, max_length=50)
    media_type: MediaTypeEnum
    description: str = Field(min_length=0, max_length=200)
    tips: str = ""
    config: str = ""


class PatchLabelTaskIn(CustomBaseModel):
    name: str | None = Field(min_length=1, max_length=50, default=None)
    media_type: MediaTypeEnum | None = None
    description: str | None = Field(min_length=0, max_length=200, default=None)
    tips: str | None = None
    config: str | None = None


class _LabelTaskSampleIn(CustomBaseModel):
    attachement_ids: list[int]
    data: dict[str, Any]


class LabelTaskSampleIn(CustomBaseModel):
    items: list[_LabelTaskSampleIn]


class PatchLabelTaskSampleIn(CustomBaseModel):
    data: dict[str, Any] | None = None
    annotated_count: int | None = None
    urls: dict[str, Any] | None = None
    state: LabelTaskSampleStateEnum | None = None
