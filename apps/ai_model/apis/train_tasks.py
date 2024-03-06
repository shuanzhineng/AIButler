from fastapi import APIRouter, Depends, Body
from common.depends import NeedAuthorization, data_range_permission, inner_authentication
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute
import aiofiles  # noqa
from http import HTTPStatus
from apps.ai_model.models.db import TrainTaskGroup, TrainTask
from apps.ai_model.models import request, response
from apps.data.models.db import DataSet
from tortoise.functions import Count
from common.utils import get_instance
from common.enums import TrainStatusEnum
from celery_app.tasks import train

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


@router.get("", summary="训练任务组列表", response_model=Page[response.TrainTaskGroupOut])
async def get_train_task_groups(query_sets=Depends(data_range_permission(TrainTaskGroup)), params=Depends(Params)):
    """训练任务组列表"""
    query_sets = query_sets.prefetch_related("creator")
    output = await paginate(query_sets, params=params)
    for item in output.items:
        counts = (
            await TrainTask.filter(train_task_group_id=item.id)
            .group_by("status")
            .annotate(status_count=Count("id"))
            .values_list("status", "status_count")
        )
        task_count_stat = {status: count for status, count in counts}
        item.task_count_stat = task_count_stat
    return output


@router.get("/{pk}", summary="训练任务组详情", response_model=response.TrainTaskGroupOut)
async def retrieve_train_task_group(
    pk: int,
    query_sets=Depends(data_range_permission(TrainTaskGroup)),
):
    """创建训练任务组"""
    instance = await get_instance(query_sets, pk)
    await instance.fetch_related("creator")
    counts = (
        await TrainTask.filter(train_task_group_id=instance.id)
        .group_by("status")
        .annotate(status_count=Count("id"))
        .values_list("status", "status_count")
    )
    task_count_stat = {status: count for status, count in counts}
    instance.task_count_stat = task_count_stat
    return instance


@router.put("/{pk}", summary="修改训练任务组", response_model=response.TrainTaskGroupOut)
async def put_train_task_group(
    pk: int,
    items: request.PutTrainTaskGroupIn,
    user: NeedAuthorization,
    query_sets=Depends(data_range_permission(TrainTaskGroup)),
):
    """创建训练任务组"""
    await get_instance(query_sets, pk)
    await query_sets.filter(id=pk).update(**items.model_dump(), modifier=user)
    instance = await query_sets.get(id=pk)
    await instance.fetch_related("creator")
    counts = (
        await TrainTask.filter(train_task_group_id=instance.id)
        .group_by("status")
        .annotate(status_count=Count("id"))
        .values_list("status", "status_count")
    )
    task_count_stat = {status: count for status, count in counts}
    instance.task_count_stat = task_count_stat
    return instance


@router.delete("/{pk}", summary="删除训练任务组")
async def delete_train_task_group(pk: int, query_sets=Depends(data_range_permission(TrainTaskGroup))):
    """创建训练任务组"""
    instance = await get_instance(query_sets, pk)
    await TrainTask.filter(train_task_group_id=instance.id).delete()
    await instance.delete()
    return


@router.post(
    "/{group_id}/tasks", summary="创建训练任务", response_model=response.TrainTaskOut, status_code=HTTPStatus.CREATED
)
async def create_train_task(
    group_id: int,
    user: NeedAuthorization,
    items: request.TrainTaskIn,
    query_sets=Depends(data_range_permission(TrainTaskGroup)),
):
    """创建训练任务组"""
    group = await get_instance(query_sets, group_id)
    items = items.model_dump()
    data_set_ids = items.pop("data_set_ids")
    data_sets = await DataSet.filter(id__in=data_set_ids)
    instance = await TrainTask.create(**items, creator=user, train_task_group=group)
    await instance.data_sets.add(*data_sets)
    # TODO 异步发起训练任务
    train.delay()
    await instance.fetch_related("creator")
    return instance


@router.put("/train-tasks/{task_id}/status", summary="修改训练任务状态", dependencies=[Depends(inner_authentication)])
async def put_train_task_status(task_id: int, status: TrainStatusEnum = Body()):
    """外部通过api修改训练任务状态"""
    await TrainTask.filter(id=task_id).update(status=status)
    return
