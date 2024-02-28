from common.base_pydantic import CustomBaseModel
from pydantic import Field, HttpUrl, field_validator

from apps.system.models.db import Menu, Role, Dept
from typing_extensions import TypedDict
from typing import Literal, Any
from pydantic import constr
from common.enums import MenuGenreEnum, DataScopeEnum


class CreateMenuIn(CustomBaseModel):
    """创建菜单请求体参数"""
    name: str = Field(min_length=1, max_length=30)
    icon: str = Field(min_length=0, max_length=30)
    web_path: str = Field(min_length=0, max_length=255)
    sort: int = Field(ge=0)
    is_link: bool = False
    disabled: bool = False
    link_url: str = Field(min_length=0, max_length=255)
    genre: MenuGenreEnum
    parent_id: int | None = None


class API(TypedDict):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    api: str


class PatchButtonIn(CustomBaseModel):

    name: str = Field(min_length=1, max_length=30)
    sort: int = Field(ge=0)
    disabled: bool = False
    apis: list[API] = []


class CreateRoleIn(CustomBaseModel):
    """创建角色请求体参数"""

    name: str = Field(min_length=1, max_length=30)
    key: str = Field(min_length=0, max_length=30)
    disabled: bool = False
    sort: int = Field(ge=0)
    description: str = Field(min_length=0, max_length=200)


class PutRoleIn(CustomBaseModel):
    """修改角色请求体参数"""

    data_range: DataScopeEnum
    dept_ids: list[int] = []
    menu_ids: list[int]


    @field_validator("dept_ids")
    @classmethod
    def validate_data_range(cls, v, values):
        if not v and values["data_range"] == DataScopeEnum.CUSTOM:
            raise ValueError(f"自定数据权限时 dept_ids 不能为空")
        return v


class CreateDeptIn(CustomBaseModel):
    """创建部门请求体参数"""

    name: str = Field(min_length=1, max_length=30)
    key: str = Field(min_length=0, max_length=30)
    owner: str = Field(min_length=1, max_length=30)
    phone: constr(min_length=11, max_length=11, pattern=r'^1\d{10}$')
    email: constr(pattern=r'[^@]+@[^@]+\.[^@]+')
    disabled: bool = False
    sort: int = Field(ge=0)
    description: str = Field(min_length=0, max_length=200)
    parent_id: int | None = None


