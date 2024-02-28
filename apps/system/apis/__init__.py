from fastapi import APIRouter
from apps.system.apis.menus import router as menus_router
from apps.system.apis.roles import router as roles_router


router = APIRouter(
    prefix="/system",
    tags=["系统管理"],
    responses={404: {"description": "Not found"}},
)

router.include_router(menus_router)
router.include_router(roles_router)
