from common.base_pydantic import CustomBaseModel
from pydantic import Field
from common.enums import AnnotationTypeEnum


class TrainTaskGroupIn(CustomBaseModel):
    name: str = Field(min_length=1, max_length=50)
    model_type: AnnotationTypeEnum
    description: str = Field(min_length=0, max_length=200)
