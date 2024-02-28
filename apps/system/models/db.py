
from tortoise import fields

from common.db import DBBaseModel
from tortoise.fields.base import OnDelete
from common.enums import APIMethodEnum, DataScopeEnum, MenuGenreEnum


class Dept(DBBaseModel):
    """部门"""
    name = fields.CharField(max_length=255, description="部门名称")
    key = fields.CharField(max_length=255, description="关联字符", default="")
    owner = fields.CharField(max_length=255, description="负责人")
    phone = fields.CharField(max_length=255, description="手机号")
    email = fields.CharField(max_length=255, description="邮箱")
    disabled = fields.BooleanField(description="是否禁用", default=False)
    sort = fields.IntField(description="排序号", default=1)
    description = fields.CharField(max_length=255, description="角色描述")
    parent = fields.ForeignKeyField(
        "models.Dept",
        on_delete=OnDelete.NO_ACTION,
        description="上级部门",
        null=True,
        db_constraint=False
    )

    class Meta:
        table = "dept"
        table_description = "部门"


class Menu(DBBaseModel):
    """菜单"""
    name = fields.CharField(max_length=255, description="菜单名称")
    icon = fields.CharField(max_length=255, description="图标代码", default="")
    sort = fields.IntField(description="排序号", default=1)
    is_link = fields.BooleanField(default=False, description="是否外链")
    link_url = fields.CharField(max_length=255, description="链接地址", default="")
    genre = fields.CharEnumField(enum_type=MenuGenreEnum, max_length=255, description="菜单类型")
    web_path = fields.CharField(max_length=255, description="路由地址", default="")
    disabled = fields.BooleanField(description="是否禁用", default=False)
    parent = fields.ForeignKeyField(
        "models.Menu",
        on_delete=OnDelete.NO_ACTION,
        description="上级菜单",
        null=True,
        db_constraint=False
    )
    api_perms: fields.ForeignKeyRelation["MenuAPIPermission"]

    class Meta:
        table = "menu"
        table_description = "菜单"
        ordering = ("sort",)


class Role(DBBaseModel):
    """角色"""
    name = fields.CharField(max_length=255, description="角色名称")
    key = fields.CharField(max_length=255, description="权限字符", default="")
    disabled = fields.BooleanField(description="是否禁用", default=False)
    sort = fields.IntField(description="排序号", default=1)
    description = fields.CharField(max_length=255, description="角色描述")
    data_range = fields.IntEnumField(
        enum_type=DataScopeEnum, description="数据范围", default=DataScopeEnum.ONLY_SELF
    )
    dept = fields.ManyToManyField(
        "models.Dept",  on_delete=OnDelete.NO_ACTION, description="自定义数据权限勾选的部门",
        db_constraint=False, related_name="roles"
    )
    menu = fields.ManyToManyField(
        "models.Menu",  on_delete=OnDelete.NO_ACTION, description="具备权限的菜单",
        db_constraint=False, related_name="roles"
    )

    class Meta:
        table = "role"
        table_description = "角色"


class MenuAPIPermission(DBBaseModel):
    """菜单按钮"""
    api = fields.CharField(max_length=255, description="接口地址", default="")
    method = fields.CharEnumField(
        max_length=255, description="接口请求方法", enum_type=APIMethodEnum
    )
    menu = fields.ForeignKeyField(
        "models.Menu",
        on_delete=OnDelete.NO_ACTION,
        description="菜单",
        related_name="api_perms",
        db_constraint=False,
        null=True
    )

    class Meta:
        table = "menu_api_permission"
        table_description = "菜单接口权限"


class RoleMenuPermission(DBBaseModel):
    """角色菜单权限"""
    role = fields.ForeignKeyField(
        "models.Role",
        on_delete=OnDelete.NO_ACTION,
        description="关联角色",
        db_constraint=False,
        null=True
    )
    menu = fields.ForeignKeyField(
        "models.Menu",
        on_delete=OnDelete.NO_ACTION,
        description="关联菜单",
        db_constraint=False,
        null=True
    )

    class Meta:
        table = "role_menu_permission"
        table_description = "角色菜单权限"


