from common.authentication import need_access_token, selectable_access_token
from typing import Annotated
from fastapi import Depends
from apps.system.models.db import User, Dept
from common.db import DBBaseModel
from tortoise.queryset import QuerySet
from typing import Type, Callable
from fastapi import Request
from conf.settings import settings
from common.exceptions import CommonError
from common.enums import DataScopeEnum

# 可选登录
SelectableAuthorization = Annotated[User | None, Depends(selectable_access_token)]
# 必须登录
NeedAuthorization = Annotated[User, Depends(need_access_token)]


def data_range_permission(model_class: Type[DBBaseModel]) -> Callable:
    """数据范围权限"""

    async def inner(user: User = Depends(need_access_token)) -> QuerySet:
        # 获取最大权限的角色
        role = await user.roles.all().order_by("-data_range").first()
        query_sets = model_class.all()
        if user.is_superuser:
            pass
        elif not role:  # 未绑定角色
            query_sets = query_sets.filter(creator=user)
        elif role.data_range == DataScopeEnum.ONLY_SELF:
            query_sets = query_sets.filter(creator=user)
        elif role.data_range == DataScopeEnum.ONLY_DEPARTMENT:
            if user.dept_belong:
                query_sets = query_sets.filter(dept_belong=user.dept_belong)
            else:
                query_sets = query_sets.filter(creator=user)
        elif role.data_range == DataScopeEnum.SELF_AND_SUBORDINATES:
            # 查询当前机构的所有子级机构
            if dept_belong_obj := user.dept_belong:
                depts = await Dept.get_children(parent_ids=[dept_belong_obj.id])
                query_sets = query_sets.filter(dept_belong__in=depts)
            else:
                query_sets = query_sets.filter(creator=user)
        elif role.data_range == DataScopeEnum.CUSTOM:
            depts = await role.depts.all()
            query_sets = query_sets.filter(dept_belong__in=depts)
        elif role.data_range == DataScopeEnum.ALL:
            pass
        return query_sets

    return inner


async def inner_authentication(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization != f"Bearer {settings.INNER_AUTHENTICATION_TOKEN}":
        raise CommonError.InnerAuthenticationError
    return
