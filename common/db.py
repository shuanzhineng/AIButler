"""
DB 基类
"""
from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import OnDelete


class DBBaseModel(Model):
    id = fields.BigIntField(pk=True, description="主键id")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    # is_removed = fields.BooleanField(description="是否删除", default=False)
    creator = fields.ForeignKeyField(
        "models.User",
        on_delete=OnDelete.NO_ACTION,
        description="创建人",
        null=True,
        db_constraint=False,
        related_name=False,
    )

    modifier_id = fields.BigIntField(null=True, description="修改人id")
    dept_belong_id = fields.BigIntField(null=True, description="数据归属部门id")

    class Meta:
        abstract = True
