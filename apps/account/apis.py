from typing import Annotated

from fastapi import APIRouter, Form

from apps.account.models import response
from common.authentication import (
    authenticate_user,
    create_token,
    refresh_token_to_access_token,
)
from common.custom_route import CustomRoute

router = APIRouter(
    prefix="/account", tags=["认证信息"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


@router.post("/oauth2/token", response_model=response.Token, summary="获取访问token")
async def get_access_token(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> dict[str, str]:
    user = await authenticate_user(username, password)
    output = create_token(data={"user_id": user.id})
    return output


@router.post("/oauth2/refresh_token", response_model=response.Token, summary="刷新访问token")
async def _refresh_token(refresh_token: str) -> dict[str, str]:
    """刷新token"""
    return refresh_token_to_access_token(refresh_token)
