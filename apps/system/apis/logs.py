from fastapi import APIRouter, Depends
from apps.system.models.db import LoginLog, AccessLog
from apps.system.models import response
from common.depends import data_range_permission
from fastapi_pagination import Page, Params, paginate
from common.custom_route import CustomRoute
from typing import Optional

router = APIRouter(
    prefix="/logs", tags=["日志管理"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


@router.get("/login-logs", summary="登录日志列表", response_model=Page[response.LoginLogOut])
async def login_log(
    username: str = "",
    ip_address: str = "",
    is_success: Optional[bool] = None,
    params=Depends(Params),
    query_sets=Depends(data_range_permission(LoginLog)),
):
    if username:
        query_sets = query_sets.filter(username__contains=username)
    if ip_address:
        query_sets = query_sets.filter(ip_addres__containss=ip_address)
    if is_success is not None:
        query_sets = query_sets.filter(is_success=is_success)
    query_sets = await query_sets
    return paginate(query_sets, params=params)


@router.get("/access-logs", summary="访问日志列表", response_model=Page[response.AccessLogOut])
async def access_log(
    api: str = "",
    method: str = "",
    ip_address: str = "",
    http_status_code: int | None = None,
    params=Depends(Params),
    query_sets=Depends(data_range_permission(AccessLog)),
):
    if api:
        query_sets = query_sets.filter(api=api)
    if ip_address:
        query_sets = query_sets.filter(ip_address=ip_address)
    if http_status_code is not None:
        query_sets = query_sets.filter(http_status_code=http_status_code)
    if method:
        query_sets = query_sets.filter(method=method)

    query_sets = await query_sets.prefetch_related("creator")
    return paginate(query_sets, params=params)
