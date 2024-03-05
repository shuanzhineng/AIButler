from fastapi import APIRouter, Depends
from common.depends import NeedAuthorization, data_range_permission
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute
import aiofiles  # noqa
from http import HTTPStatus
from apps.ai_model.models.db import TrainTaskGroup, TrainTask
from apps.ai_model.models import request, response

router = APIRouter(
    prefix="/train-task-groups",
    tags=["训练任务组"],
    responses={404: {"description": "Not found"}},
    route_class=CustomRoute,
)


@router.post("", summary="创建训练任务组", response_model=response.TrainTaskGroupOut, status_code=HTTPStatus.CREATED)
async def create_train_task_group(user: NeedAuthorization, items: request.TrainTaskGroupIn):
    """创建训练任务组"""
    role = await TrainTaskGroup.create(**items.model_dump(), creator=user)
    return role


@router.get("", summary="训练任务组列表", response_model=response.TrainTaskGroupOut)
async def get_train_task_groups(query_sets=Depends(data_range_permission(TrainTaskGroup)), params=Depends(Params)):
    """训练任务组列表"""
    query_sets = query_sets.prefetch_related("creator")
    output = await paginate(query_sets, params=params)
    for item in output.items:
        await TrainTask.filter(train_task_group_id=item.id).group_by("status").count()
        task_count_stat = {}
        item.task_count_stat = task_count_stat
    return output
