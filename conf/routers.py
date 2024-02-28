from fastapi import FastAPI

from apps.account.apis import router as account_router
from apps.system.apis import router as system_router


def register_router(app: FastAPI) -> None:
    # 添加路由蓝图
    app.include_router(account_router)
    app.include_router(system_router)
