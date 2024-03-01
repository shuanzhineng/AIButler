from fastapi import APIRouter, Depends
from apps.system.models.db import LoginLog, AccessLog
from apps.system.models import response
from apps.account.depends import NeedAuthorization
from fastapi_pagination import Page, Params, paginate
from common.custom_route import CustomRoute

router = APIRouter(
    prefix="/logs", tags=["日志管理"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


@router.get("/login-logs", summary="登录日志列表", response_model=Page[response.LoginLogOut])
async def login_log(
    user: NeedAuthorization,
    username: str = "",
    ip_address: str = "",
    is_success: bool | None = None,
    params=Depends(Params),
):
    query_sets = LoginLog.all()
    if username:
        query_sets = query_sets.filter(username=username)
    if ip_address:
        query_sets = query_sets.filter(ip_address=ip_address)
    if is_success is not None:
        query_sets = query_sets.filter(is_success=is_success)
    query_sets = await query_sets
    return paginate(query_sets, params=params)


@router.get("/access-logs", summary="访问日志列表", response_model=Page[response.AccessLogOut])
async def access_log(
    user: NeedAuthorization,
    api: str = "",
    method: str = "",
    ip_address: str = "",
    http_status_code: int | None = None,
    params=Depends(Params),
):
    query_sets = AccessLog.all()
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
