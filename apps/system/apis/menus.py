from fastapi import APIRouter, Depends
from apps.system.models.db import Menu, MenuAPIPermission
from apps.system.models import request, response
from apps.account.depends import NeedAuthorization
from common.utils import get_instance, construct_tree
from common.enums import MenuGenreEnum
from fastapi_pagination import Page, Params
from http import HTTPStatus
from tortoise.transactions import atomic
from fastapi_pagination.ext.tortoise import paginate
from common.custom_route import CustomRoute


router = APIRouter(
    prefix="/menus", tags=["菜单管理"], responses={404: {"description": "Not found"}}, route_class=CustomRoute
)


# TODO 增加修改人和归属部门
@router.get("", summary="菜单列表", response_model=Page[response.QueryMenuOut])
async def menus(user: NeedAuthorization, params=Depends(Params), parent_id: int | None = None):
    """index"""
    query_sets = Menu.filter(parent=parent_id, genre__in=[MenuGenreEnum.DIRECTORY, MenuGenreEnum.PAGE])
    output = await paginate(query_sets)
    # 在分页结果中修改child
    for obj in output.items:
        hava_child = bool(await Menu.filter(parent=obj.id))
        obj.child = hava_child
    return output


@router.get("/full-tree", summary="菜单树", response_model=list[response.QueryMenuTreeOut])
async def menu_tree(user: NeedAuthorization):
    """完整菜单树"""
    query_sets = await Menu.all().prefetch_related("parent")
    tree = construct_tree(query_sets)
    output = []
    for obj in tree:
        result = dict(await response.QueryMenuTreeOut.from_tortoise_orm(obj))
        output.append(result)
    return output


@router.get("/{pk}/buttons", summary="菜单按钮", response_model=Page[response.QueryButtonOut])
async def buttons(pk: int, user: NeedAuthorization, params=Depends(Params)):
    """菜单下的按钮"""
    query_sets = Menu.filter(parent=pk, genre=MenuGenreEnum.BUTTON)
    output = await paginate(query_sets)
    for obj in output.items:
        menu = await Menu.get(pk=obj.id)
        obj.apis = list(await menu.api_perms.all().values("method", "api"))
    return output


@router.put("/buttons/{pk}", summary="修改按钮", response_model=response.QueryButtonOut)
async def put_button(pk: int, items: request.PatchButtonIn, user: NeedAuthorization):
    """修改按钮"""
    instance = await get_instance(Menu, pk)
    items = items.model_dump()

    @atomic()
    async def _patch():
        nonlocal instance
        apis = items.pop("apis")
        items["modifier_id"] = user.id
        await Menu.filter(id=instance.id).update(**items)
        api_perms = await instance.api_perms.all()
        for api_perm in api_perms:
            await api_perm.delete()
        bulk_data = []
        for api in apis:
            bulk_data.append(MenuAPIPermission(**api, menu=instance))
        await MenuAPIPermission.bulk_create(bulk_data)
        instance = await get_instance(Menu, pk)
        output = dict(await response.QueryButtonOut.from_tortoise_orm(instance))
        apis = [{"method": api_perm.method.value, "api": api_perm.api} for api_perm in api_perms]
        output["apis"] = apis
        return output

    output = await _patch()
    return output


@router.delete("/buttons/{pk}", summary="删除按钮")
async def delete_button(pk: int, items: request.PatchButtonIn, user: NeedAuthorization, params=Depends(Params)):
    """删除按钮"""
    instance = await get_instance(Menu, pk)

    @atomic()
    async def _delete():
        nonlocal instance
        api_perms = await instance.api_perms.all()
        for api_perm in api_perms:
            await api_perm.delete()
        await instance.delete()

    await _delete()
    return


@router.get("/{pk}", summary="菜单详情", response_model=response.MenuDetailOut)
async def retrieve_menu(pk: int, user: NeedAuthorization):
    """查看菜单详情"""
    instance = await get_instance(Menu, pk)
    output = dict(await response.MenuNoParentOut.from_tortoise_orm(instance))
    parent = await instance.parent
    output["parent"] = None
    while parent:
        if parent:
            output["parent"] = dict(await response.MenuNoParentOut.from_tortoise_orm(parent))
            parent = await parent.parent
        else:
            output["parent"] = None
            break
    return output


@router.post("", summary="创建菜单", response_model=response.MenuDetailOut, status_code=HTTPStatus.CREATED)
async def create_menu(user: NeedAuthorization, items: request.CreateMenuIn):
    """创建菜单"""
    instance = await Menu.create(**items.model_dump(), creator=user)
    output = dict(await response.MenuNoParentOut.from_tortoise_orm(instance))
    parent = await instance.parent
    output["parent"] = None
    while parent:
        if parent:
            output["parent"] = dict(await response.MenuNoParentOut.from_tortoise_orm(parent))
            parent = await parent.parent
        else:
            output["parent"] = None
            break
    return output


@router.put("/{pk}", summary="修改菜单", response_model=response.MenuDetailOut)
async def put_menu(pk: int, user: NeedAuthorization, items: request.CreateMenuIn):
    """修改菜单"""
    instance = await get_instance(Menu, pk)
    items = items.model_dump()
    items["modifier_id"] = user.id
    parent_id = items.pop("parent_id")
    parent = await Menu.get(id=parent_id)
    await Menu.filter(id=instance.id).update(**items, parent=parent)
    instance = await Menu.get(id=pk)
    output = dict(await response.MenuNoParentOut.from_tortoise_orm(instance))
    parent = await instance.parent
    output["parent"] = None
    while parent:
        if parent:
            output["parent"] = dict(await response.MenuNoParentOut.from_tortoise_orm(parent))
            parent = await parent.parent
        else:
            output["parent"] = None
            break
    return output


@router.delete("/{pk}", summary="删除菜单")
async def delete_menu(pk: int, user: NeedAuthorization):
    """删除菜单"""
    instance = await get_instance(Menu, pk)
    await Menu.filter(parent=instance).update(parent=None)
    await instance.delete()
    return
