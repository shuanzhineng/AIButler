from typing import Annotated, Type

from fastapi import APIRouter, Depends
from apps.system.models.db import Menu, MenuAPIPermission, Role, Dept
from apps.system.models import request, response
from apps.account.depends import NeedAuthorization
from common.utils import get_instance, construct_tree
from common.enums import MenuGenreEnum, DataScopeEnum
from fastapi_pagination import Page, Params
from loguru import logger
from http import HTTPStatus
from tortoise.transactions import atomic
from fastapi_pagination.ext.tortoise import paginate

router = APIRouter(
    prefix="/depts",
    tags=["部门管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("", summary="部门列表", response_model=Page[response.DeptNoParentOut])
async def depts(user: NeedAuthorization):
    """部门列表"""
    return await paginate(Dept.all())


@router.get("/{pk}", summary="部门详情", response_model=response.DeptDetailOut)
async def retrieve_dept(pk: int, user: NeedAuthorization):
    """部门详情"""
    instance = await get_instance(Dept, pk)
    output = dict(await response.DeptNoParentOut.from_tortoise_orm(instance))
    parent = await instance.parent
    output["parent"] = None
    while parent:
        if parent:
            output["parent"] = dict(await response.DeptNoParentOut.from_tortoise_orm(parent))
            parent = await parent.parent
        else:
            output["parent"] = None
            break
    return instance


@router.post("", summary="创建部门",  response_model=response.DeptDetailOut, status_code=HTTPStatus.CREATED)
async def create_dept(user: NeedAuthorization, items: request.CreateDeptIn):
    """创建部门"""
    instance = await Dept.create(**items.model_dump(), creator=user)
    output = dict(await response.DeptNoParentOut.from_tortoise_orm(instance))
    parent = await instance.parent
    output["parent"] = None
    while parent:
        if parent:
            output["parent"] = dict(await response.DeptNoParentOut.from_tortoise_orm(parent))
            parent = await parent.parent
        else:
            output["parent"] = None
            break
    return output


@router.put("/{pk}", summary="修改部门", response_model=response.DeptNoParentOut)
async def put_dept(pk: int, user: NeedAuthorization, items: request.CreateDeptIn):
    """修改部门"""
    instance = await get_instance(Role, pk)
    await Role.filter(id=instance.id).update(**items.model_dump())
    return instance


@router.delete("/{pk}", summary="删除角色")
async def delete_dept(pk: int, user: NeedAuthorization):
    """删除部门"""
    instance = await get_instance(Role, pk)
    await instance.delete()
    return
