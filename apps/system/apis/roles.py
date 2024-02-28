from fastapi import APIRouter
from apps.system.models.db import Menu, Role, Dept
from apps.system.models import request, response
from apps.account.depends import NeedAuthorization
from common.utils import get_instance
from fastapi_pagination import Page
from http import HTTPStatus
from tortoise.transactions import atomic
from fastapi_pagination.ext.tortoise import paginate

router = APIRouter(
    prefix="/roles",
    tags=["角色管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("", summary="角色列表", response_model=Page[response.RoleOut])
async def roles(user: NeedAuthorization):
    """角色列表"""
    return await paginate(Role.all())


@router.get("/{pk}", summary="角色详情", response_model=response.RoleOut)
async def retrieve_role(pk: int, user: NeedAuthorization):
    """角色详情"""
    instance = await get_instance(Role, pk)
    return instance


@router.post("", summary="创建角色", response_model=response.RoleOut, status_code=HTTPStatus.CREATED)
async def create_role(user: NeedAuthorization, items: request.CreateRoleIn):
    """创建角色"""
    role = await Role.create(**items.model_dump(), creator=user)
    return role


@router.put("/{pk}", summary="修改角色", response_model=response.RoleOut)
async def put_role(pk: int, user: NeedAuthorization, items: request.CreateRoleIn):
    """修改角色"""
    instance = await get_instance(Role, pk)
    await Role.filter(id=instance.id).update(**items.model_dump())
    return instance


@router.patch("/{pk}/permission", summary="修改角色权限")
async def patch_role_permission(pk: int, user: NeedAuthorization, items: request.PutRoleIn):
    """修改角色权限"""
    instance = await get_instance(Role, pk)
    items = items.model_dump()

    @atomic()
    async def _patch():
        instance.data_range = items["data_range"]
        await instance.save()
        menu_ids = items["menu_ids"]
        dept_ids = items["dept_ids"]

        menu_objs = await Menu.filter(id__in=menu_ids)
        dept_objs = await Dept.filter(id__in=dept_ids)

        await instance.menu.clear()
        await instance.dept.clear()
        await instance.menu.add(menu_objs)
        await instance.dept.add(dept_objs)

    await _patch()
    return


@router.delete("/{pk}", summary="删除角色")
async def delete_role(pk: int, user: NeedAuthorization):
    """删除角色"""
    instance = await get_instance(Role, pk)
    await instance.delete()
    return
