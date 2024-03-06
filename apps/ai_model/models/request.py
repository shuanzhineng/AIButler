from common.base_pydantic import CustomBaseModel
from pydantic import Field
from common.enums import AnnotationTypeEnum


class TrainTaskGroupIn(CustomBaseModel):
    name: str = Field(min_length=1, max_length=50)
    ai_model_type: AnnotationTypeEnum
    description: str = Field(min_length=0, max_length=200)


class PutTrainTaskGroupIn(CustomBaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=0, max_length=200)


class TrainTaskIn(CustomBaseModel):
    description: str = Field(min_length=0, max_length=200)
    params: dict
    base_task_id: int | None = None
    data_set_ids: list = []
