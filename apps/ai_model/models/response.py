from common.base_pydantic import CreatorOut, custom_base_model_config
from pydantic import field_validator
from apps.ai_model.models.db import TrainTaskGroup
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from common.enums import AnnotationTypeEnum

# ---------------------标注任务model------------------------
_TrainTaskGroupOut = pydantic_model_creator(
    TrainTaskGroup, name="_TrainTaskGroupOut", model_config=custom_base_model_config
)


class TrainTaskGroupOut(_TrainTaskGroupOut):  # type: ignore
    creator: CreatorOut | None = None
    task_count_stat: dict = {}

    @field_validator(
        "model_type",
    )
    @classmethod
    def change_data_type(cls, v):
        if not isinstance(v, dict):
            return {"name": AnnotationTypeEnum.get_display(v), "value": v}
        return v
