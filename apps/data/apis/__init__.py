from fastapi import APIRouter
from apps.data.apis.label_task import router as label_tasks_router


router = APIRouter(
    prefix="/data",
    tags=["数据管理"],
    responses={404: {"description": "Not found"}},
)

router.include_router(label_tasks_router)
