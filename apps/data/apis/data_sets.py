from fastapi import APIRouter, Depends
from apps.data.models.db import DataSetGroup, DataSet, OssFile
from apps.data.models import request, response
from common.depends import NeedAuthorization, data_range_permission
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute
from common.minio_client import minio_client
from common.utils import get_instance
from asyncer import asyncify
from common.utils import get_current_time


router = APIRouter(
    prefix="/data-set-groups", tags=["数据集"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


@router.get("/presigned-upload-url", summary="获取预上传url")
async def get_presigned_upload_url(filename: str, user: NeedAuthorization):
    """标注任务列表"""
    datetime = get_current_time().strftime("%Y-%m")
    oss_path = f"{user.username}/{datetime}/{filename}"
    file_obj = await OssFile.create(path=oss_path, filename=filename, creator=user)

    presigned_upload_url = await asyncify(minio_client.presigned_upload_file)(oss_path)
    return {"presigned_upload_url": presigned_upload_url, "file_id": file_obj.id}


@router.get("", summary="数据集组", response_model=Page[response.DataSetGroupOut])
async def data_set_groups(query_sets=Depends(data_range_permission(DataSetGroup)), params=Depends(Params)):
    """数据集组列表"""
    query_sets = query_sets.prefetch_related("creator")
    output = await paginate(query_sets, params=params)
    for item in output.items:
        item.data_set_count = await DataSet.filter(data_set_group_id=item.id).count()
    return output


@router.post("", summary="数据集组", response_model=response.DataSetGroupOut)
async def create_data_set_group(user: NeedAuthorization, items: request.DataSetGroupIn):
    """创建数据集"""
    instance = await DataSetGroup.create(**items.model_dump(), creator=user)
    await instance.fetch_related("creator")
    return instance


@router.put("/{pk}", summary="修改数据集组", response_model=response.DataSetGroupOut)
async def put_data_set_group(
    pk: int,
    user: NeedAuthorization,
    items: request.DataSetGroupIn,
    query_sets=Depends(data_range_permission(DataSetGroup)),
):
    """创建数据集"""
    await get_instance(query_sets, pk)
    await query_sets.filter(id=pk).update(**items.model_dump(), modifier=user)
    instance = await query_sets.get(id=pk)
    await instance.fetch_related("creator")
    instance.data_set_count = await DataSet.filter(data_set_group_id=pk).count()
    return instance


@router.get("/{pk}", summary="数据集组详情", response_model=response.DataSetGroupOut)
async def retrieve_data_set_group(pk: int, query_sets=Depends(data_range_permission(DataSetGroup))):
    """创建数据集"""
    instance = await get_instance(query_sets, pk)
    await instance.fetch_related("creator")
    instance.data_set_count = await DataSet.filter(data_set_group_id=instance.id).count()
    return instance


@router.delete("/{pk}", summary="删除数据集组")
async def delete_data_set_group(pk: int, query_sets=Depends(data_range_permission(DataSetGroup))):
    """创建数据集"""
    instance = await get_instance(query_sets, pk)
    await DataSet.filter(data_set_group_id=instance.id).delete()
    await instance.delete()
    return


@router.post("/{group_id}/data-sets", summary="创建数据集", response_model=response.DataSetOut)
async def create_data_set(
    group_id: int,
    user: NeedAuthorization,
    items: request.DataSetIn,
    query_sets=Depends(data_range_permission(DataSetGroup)),
):
    """创建数据集"""
    group = await get_instance(query_sets, group_id)
    items = items.model_dump()
    oss_file = await get_instance(OssFile, items.pop("file_id"))
    version = 1
    data_set = await DataSet.filter(data_set_group=group).order_by("-version").first()
    if data_set:
        version = data_set.version + 1
    instance = await DataSet.create(**items, data_set_group=group, creator=user, version=version, oss_file=oss_file)
    instance.filename = oss_file.filename
    return instance


@router.get("/{group_id}/data-sets/{pk}/download-url", summary="下载数据集")
async def download_data_set(
    group_id: int,
    pk: int,
    query_sets=Depends(data_range_permission(DataSetGroup)),
    data_set_query_sets=Depends(data_range_permission(DataSet)),
):
    """下载数据集"""
    await get_instance(query_sets, group_id)
    data_set_obj = await get_instance(data_set_query_sets, pk)
    oss_path = await data_set_obj.file.path
    presigned_download_url = minio_client.presigned_download_file(oss_path)
    return {"presigned_download_url": presigned_download_url}
