from common.base_pydantic import CustomBaseModel
from pydantic import field_validator
from typing import Literal
from typing_extensions import TypedDict
from apps.system.models.db import Menu, Role, Dept, User
from common.enums import MenuGenreEnum
from tortoise.contrib.pydantic.creator import pydantic_model_creator

# ---------------------菜单model------------------------
_MenuNoParentOut = pydantic_model_creator(Menu, name="_MenuNoParentOut", allow_cycles=True, exclude=("parent",))


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


class MenuNoParentOut(_MenuNoParentOut, CustomBaseModel):  # type: ignore
    genre: dict[str, str] | str

    @field_validator(
        "genre",
    )
    @classmethod
    def change_genre(cls, v):
        if not isinstance(v, dict):
            return {"name": MenuGenreEnum.get_display(v), "value": v}
        return v


class MenuDetailOut(MenuNoParentOut):
    """创建菜单响应体参数"""

    parent: dict | None


class QueryMenuOut(MenuNoParentOut):
    """查询菜单响应体参数"""

    child: bool = False


class QueryMenuTreeOut(MenuNoParentOut):
    """查询菜单树响应体参数"""

    children: list["QueryMenuTreeOut"] = []


class QueryButtonOut(_ButtonNoParentOut, CustomBaseModel):  # type: ignore
    """查询菜单响应体参数"""

    class API(TypedDict):
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
        api: str

    apis: list[API] = []


# ---------------------角色model------------------------

_RoleOut = pydantic_model_creator(
    Role,
    name="_RoleOut",
)


class RoleOut(_RoleOut, CustomBaseModel):  # type: ignore
    pass


# ---------------------部门model------------------------

_DeptNoParentOut = pydantic_model_creator(Dept, name="_DeptNoParentOut", allow_cycles=True, exclude=("parent",))


class DeptNoParentOut(_DeptNoParentOut, CustomBaseModel):  # type: ignore
    pass


class QueryDeptOut(DeptNoParentOut):
    """查询菜单响应体参数"""

    child: bool = False


class DeptDetailOut(DeptNoParentOut, CustomBaseModel):
    parent: dict | None = None


class QueryDeptTreeOut(DeptNoParentOut):
    """查询菜单树响应体参数"""

    children: list["QueryDeptTreeOut"] = []


# ---------------------用户model------------------------

_UserOut = pydantic_model_creator(User, name="_UserOut", exclude=("password",))


class UserOut(_UserOut, CustomBaseModel):  # type: ignore
    roles: list[RoleOut] = []
    depts: list[DeptNoParentOut] = []
