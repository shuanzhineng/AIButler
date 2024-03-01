from common.enums import LabelTaskStatusEnum, MediaTypeEnum, LabelTaskSampleStateEnum

from tortoise import fields
from tortoise.fields.base import OnDelete

from common.db import DBBaseModel


class LabelTask(DBBaseModel):
    """标注任务"""

    name = fields.CharField(description="任务名称", max_length=255)
    description = fields.CharField(description="标注任务描述", max_length=255, default="")
    tips = fields.TextField(description="标注任务提示", default="")
    config = fields.TextField(description="任务配置yaml", default="")
    media_type = fields.CharEnumField(
        MediaTypeEnum, description="数据类型", max_length=255, default=MediaTypeEnum.IMAGE
    )
    status = fields.CharEnumField(
        LabelTaskStatusEnum, description="任务状态", max_length=255, default=LabelTaskStatusEnum.DRAFT
    )
    last_sample_inner_id = fields.IntField(description="任务中样本的最后一个内部id", default=0)

    class Meta:
        table = "label_task"
        table_description = "标注任务"


class LabelTaskAttachment(DBBaseModel):
    """标注任务附件"""

    file_path = fields.CharField(description="文件path", max_length=255, default="")
    local_file_path = fields.CharField(description="本地文件path", max_length=255, default="")
    label_task = fields.ForeignKeyField(
        "models.LabelTask", on_delete=OnDelete.NO_ACTION, description="标注任务", null=True, db_constraint=False
    )

    class Meta:
        table = "label_task_attachment"
        table_description = "标注任务附件"


class LabelTaskSample(DBBaseModel):
    """标注任务样本"""

    task_attachment_ids = fields.CharField(description="任务附件id", max_length=255)
    annotated_count = fields.IntField(description="样本标注数", default=0)
    data = fields.JSONField(description="标注结果", default=dict)
    state = fields.CharEnumField(
        LabelTaskSampleStateEnum, description="标注状态", max_length=255, default=LabelTaskSampleStateEnum.NEW
    )
    label_task = fields.ForeignKeyField(
        "models.LabelTask", on_delete=OnDelete.NO_ACTION, description="标注任务", null=True, db_constraint=False
    )

    class Meta:
        table = "label_task_sample"
        table_description = "标注任务样本"
