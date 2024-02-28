from common.authentication import need_access_token, selectable_access_token
from typing import Annotated
from fastapi import Depends
from apps.system.models.db import User

# 可选登录
SelectableAuthorization = Annotated[User | None, Depends(selectable_access_token)]
# 必须登录
NeedAuthorization = Annotated[User, Depends(need_access_token)]
