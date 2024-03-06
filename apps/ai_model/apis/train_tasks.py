from fastapi import APIRouter, Depends, Body
from common.depends import NeedAuthorization, data_range_permission, inner_authentication
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute
import aiofiles  # noqa
from http import HTTPStatus
from apps.ai_model.models.db import TrainTaskGroup, TrainTask
from apps.ai_model.models import request, response
from apps.data.models.db import DataSet, OssFile
from tortoise.functions import Count
from common.utils import get_instance, get_current_time
from common.enums import TrainStatusEnum
from celery_app.tasks import train
from common.minio_client import minio_client
from asyncer import asyncify

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
    base_task_id = items.pop("base_task_id")
    base_task = await TrainTask.filter(id=base_task_id).first()
    data_sets = await DataSet.filter(id__in=data_set_ids)
    instance = await TrainTask.create(**items, creator=user, train_task_group=group, base_task=base_task)
    await instance.data_sets.add(*data_sets)
    # 异步发起训练任务
    data_set_urls = []
    for data_set_obj in data_sets:
        file = await data_set_obj.file
        download_url = await asyncify(minio_client.presigned_download_file)(file.path)
        data_set_urls.append(download_url)
    pretrain_model_weight_download_url = None
    if base_task:
        pretrain_model_weight_download_url = await asyncify(minio_client.presigned_download_file)(
            base_task.result_file.path
        )
    year_month = get_current_time().strftime("%Y-%m")
    model_weight_oss_path = f"{user.username}/train/{year_month}/{instance.id}/result.zip"
    train_log_oss_path = f"{user.username}/train/{year_month}/{instance.id}/train.log"
    result_file = await OssFile.create(path=model_weight_oss_path)
    log_file = await OssFile.create(path=train_log_oss_path)
    instance.result_file = result_file
    instance.log_file = log_file
    await instance.save()
    model_weight_upload_url = await asyncify(minio_client.presigned_upload_file)(result_file.path)
    log_upload_url = await asyncify(minio_client.presigned_upload_file)(log_file.path)
    train.delay(
        train_task_id=str(instance.id),
        data_set_urls=data_set_urls,
        pretrain_model_weight_download_url=pretrain_model_weight_download_url,
        train_params=items["params"],
        model_weight_upload_url=model_weight_upload_url,
        log_upload_url=log_upload_url,
    )
    await instance.fetch_related("creator")
    return instance


@router.put("/train-tasks/{task_id}/status", summary="修改训练任务状态", dependencies=[Depends(inner_authentication)])
async def put_train_task_status(task_id: int, status: TrainStatusEnum = Body()):
    """外部通过api修改训练任务状态"""
    await TrainTask.filter(id=task_id).update(status=status)
    return
