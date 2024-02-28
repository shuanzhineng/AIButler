from common.base_pydantic import CustomBaseModel
from pydantic import Field, HttpUrl, field_validator
from typing import Literal
from typing_extensions import TypedDict
from apps.system.models.db import Menu, Role, Dept
from common.enums import MenuGenreEnum
from tortoise.contrib.pydantic.creator import pydantic_model_creator


_MenuNoParentOut = pydantic_model_creator(
    Menu,
    name="_MenuNoParentOut",
    allow_cycles=True,
    exclude=("parent", )
)


_ButtonNoParentOut = pydantic_model_creator(
    Menu,
    name="_ButtonNoParentOut",
    include=(
        "id",
        "name",
        "sort",
        "disabled",
    ),

)


_DeptNoParentOut = pydantic_model_creator(
    Dept,
    name="_DeptNoParentOut",
    allow_cycles=True,
    exclude=("parent", )
)

_RoleOut = pydantic_model_creator(
    Role,
    name="_RoleOut",

)

_DeptOut = pydantic_model_creator(
    Dept,
    name="_DeptOut",

)


class MenuNoParentOut(_MenuNoParentOut, CustomBaseModel):
    pass


class DeptNoParentOut(_DeptNoParentOut, CustomBaseModel):
    pass


class MenuDetailOut(MenuNoParentOut):
    """创建菜单响应体参数"""
    parent: dict | None

    @field_validator(
        "genre",
    )
    @classmethod
    def change_genre(cls, v):
        return {
            "name": MenuGenreEnum.get_display(v),
            "value": v
        }


class QueryMenuOut(MenuNoParentOut):
    """查询菜单响应体参数"""
    child: bool = False


class QueryMenuTreeOut(MenuNoParentOut):
    """查询菜单树响应体参数"""
    children: list["QueryMenuTreeOut"] = []


class QueryButtonOut(_ButtonNoParentOut, CustomBaseModel):
    """查询菜单响应体参数"""
    class API(TypedDict):
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
        api: str

    apis: list[API] = []


class RoleOut(_RoleOut, CustomBaseModel):
    pass


class DeptDetailOut(_DeptOut, CustomBaseModel):
    parent: dict | None
