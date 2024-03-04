from common.authentication import need_access_token, selectable_access_token
from typing import Annotated
from fastapi import Depends
from apps.system.models.db import User
from common.db import DBBaseModel
from tortoise.queryset import QuerySet
from typing import Type, Callable

# 可选登录
SelectableAuthorization = Annotated[User | None, Depends(selectable_access_token)]
# 必须登录
NeedAuthorization = Annotated[User, Depends(need_access_token)]


def data_range_permission(model_class: Type[DBBaseModel]) -> Callable:
    """数据范围权限"""

    async def inner(user: User = Depends(need_access_token)) -> QuerySet:
        # roles = await user.roles.all()
        return model_class.all()

    return inner
