from fastapi import APIRouter, Depends, Form, UploadFile, Body
from apps.data.models.db import LabelTask, LabelTaskAttachment, LabelTaskSample
from apps.data.models import request, response
from apps.account.depends import NeedAuthorization
from fastapi_pagination import Page, Params
from typing import Any
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute
from common.utils import get_instance
import os
from tortoise.exceptions import DoesNotExist
from common.exceptions import CommonError
import aiofiles  # noqa

router = APIRouter(
    prefix="/label-tasks", tags=["数据标注"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


@router.get("", summary="标注任务列表", response_model=Page[response.LabelTaskOut])
async def label_tasks(user: NeedAuthorization, params=Depends(Params)):
    """标注任务列表"""
    query_sets = LabelTask.all().prefetch_related("creator")
    return await paginate(query_sets, params=params)


@router.post("", summary="创建标注任务", response_model=response.LabelTaskOut)
async def create_label_task(user: NeedAuthorization, items: request.LabelTaskIn):
    """创建标注任务"""
    instance = await LabelTask.create(**items.model_dump(), creator=user)
    await instance.fetch_related("creator")
    return instance


@router.get("/{pk}", summary="标注任务详情", response_model=response.LabelTaskOut)
async def retrieve_label_task(
    pk: int,
    user: NeedAuthorization,
):
    """创建标注任务"""
    instance = await get_instance(LabelTask, pk)
    await instance.fetch_related("creator")
    return instance


@router.patch("/{pk}", summary="修改标注任务", response_model=response.LabelTaskOut)
async def patch_label_task(pk: int, user: NeedAuthorization, items: request.PatchLabelTaskIn):
    """修改标注任务"""
    items = items.model_dump()
    instance = await get_instance(LabelTask, pk)
    for key, v in items.items():
        if v is not None:
            setattr(instance, key, v)
    instance.modifier = user
    await instance.save()
    await instance.fetch_related("creator")
    return instance


@router.delete("/{pk}", summary="删除标注任务")
async def delete_label_task(pk: int, user: NeedAuthorization):
    """删除标注任务"""
    instance = await get_instance(LabelTask, pk)
    await instance.delete()
    return


@router.post("/{pk}/attachments", summary="上传标注任务附件")
async def label_task_attachments(
    pk: int, user: NeedAuthorization, file: UploadFile, dir_name: str | None = Form(default=None)
) -> dict[str, Any]:
    """上传标注任务附件"""
    instance = await get_instance(LabelTask, pk)
    attachment_obj = await LabelTaskAttachment.create(label_task=instance, creator=user)
    filename = file.filename
    if dir_name:
        path = f"static/labelu/{instance.id}/{dir_name}/"
        attachment_obj.local_file_path = f"{dir_name}/" + filename
    else:
        path = f"static/labelu/{instance.id}/"
        attachment_obj.local_file_path = filename
    os.makedirs(path, exist_ok=True)
    async with aiofiles.open(path + filename, "wb") as f:
        await f.write(await file.read())
    attachment_obj.file_path = "/" + path + filename
    await attachment_obj.save()
    return {
        "id": attachment_obj.id,
        "url": attachment_obj.file_path,
        "local_path": attachment_obj.local_file_path,
        "label_task": {
            "id": instance.id,
            "name": instance.name,
        },
    }


@router.delete("/{pk}/bulk-delete-attachments", summary="批量删除附件")
async def delete_label_task_attachments(pk: int, user: NeedAuthorization, attachment_ids: list[int] = Body()):
    """删除标注任务附件"""
    await get_instance(LabelTask, pk)
    file_paths = await LabelTaskAttachment.filter(id__in=attachment_ids).values_list("file_path")
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
    await LabelTaskAttachment.filter(id__in=attachment_ids).delete()
    return


@router.post("/{pk}/samples", summary="附件转为标注样本")
async def create_label_sample(
    pk: int,
    user: NeedAuthorization,
    items: request.LabelTaskSampleIn,
):
    """附件转为标注样本"""
    label_task = await get_instance(LabelTask, pk)
    data = items.model_dump()["items"]
    ids = []
    for d in data:
        sample_obj = await LabelTaskSample.create(
            task_attachment_ids=d["attachement_ids"], data=d["data"], label_task=label_task, creator=user
        )
        ids.append(sample_obj.id)
    return {"ids": ids}


@router.get("/{pk}/samples", summary="标注样本列表", response_model=Page[response.LabelTaskSampleOut])
async def label_samples(pk: int, user: NeedAuthorization, params=Depends(Params)):
    """标注样本列表"""
    label_task = await get_instance(LabelTask, pk)
    query_sets = LabelTaskSample.filter(label_task=label_task)
    return await paginate(query_sets, params=params)


@router.get("/{task_id}/samples/{sample_id}", summary="标注样本详情", response_model=response.LabelTaskSampleOut)
async def retrieve_label_sample(
    task_id: int,
    sample_id: int,
    user: NeedAuthorization,
):
    """标注样本列表"""
    try:
        instance = await LabelTaskSample.get(label_task_id=task_id, id=sample_id)
    except DoesNotExist:
        raise CommonError.ResourceDoesNotExistError
    return instance


@router.patch("/{task_id}/samples/{sample_id}", summary="标注样本详情", response_model=response.LabelTaskSampleOut)
async def patch_label_sample(
    task_id: int,
    sample_id: int,
    user: NeedAuthorization,
    items: request.PatchLabelTaskSampleIn,
):
    """修改标注样本"""
    try:
        instance = await LabelTaskSample.get(label_task_id=task_id, id=sample_id)
    except DoesNotExist:
        raise CommonError.ResourceDoesNotExistError
    if items.data is not None:
        instance.data = items.data
    for key, v in items.model_dump().items():
        if v is not None:
            setattr(instance, key, v)
    await instance.save()
    return instance
