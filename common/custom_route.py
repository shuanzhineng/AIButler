from fastapi.routing import APIRoute
from typing import Callable
from fastapi import Response, Request
from apps.system.models.db import AccessLog, LoginLog
from ua_parser.user_agent_parser import Parse

from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt

from apps.system.models.db import User
from conf.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

AUTH_USER_MODEL = User
LOGIN_PATH = "/account/oauth2/token"
NO_LOG_PATH: list[str] = []  # 登录接口和涉及文件上传和下载的接口不记录日志


class CustomRoute(APIRoute):
    """自定义路由处理"""

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            response_body = response.body
            user_agent = request.headers["user-agent"]
            parsed_user_agent = Parse(user_agent)
            user_agent = parsed_user_agent["user_agent"]
            os_info = parsed_user_agent["os"]
            browser = ""
            os = ""
            if family := user_agent.get("family"):
                browser = f"{family} {user_agent.get('major')}.{user_agent.get('minor')}.{user_agent.get('patch')}"
            if family := os_info.get("family"):
                os = f"{family} {os_info.get('major')}.{os_info.get('minor')}.{os_info.get('patch')}"

            if request.url.path == LOGIN_PATH:
                request_form = dict(await request.form())
                await LoginLog.create(
                    username=request_form["username"],
                    ip_address=request.client.host,
                    browser=browser,
                    os=os,
                    http_status_code=response.status_code,
                    is_success=True if response.status_code == 200 else False,
                )
            elif request.url.path not in NO_LOG_PATH:
                # 记录访问日志
                request_body: bytes = await request.body()
                # 提取操作人
                authorization = request.headers.get("Authorization")
                _, token = get_authorization_scheme_param(authorization)
                user = None
                if token:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    user_id = payload.get("user_id")
                    user = await User.filter(id=user_id).first()
                await AccessLog.create(
                    api=request.url.path + "?" + request.url.query,
                    method=request.method,
                    ip_address=request.client.host,
                    browser=browser,
                    os=os,
                    http_status_code=response.status_code,
                    request_body=request_body.decode(),
                    response_body=response_body.decode(),
                    creator=user,
                )
            return response

        return custom_route_handler
