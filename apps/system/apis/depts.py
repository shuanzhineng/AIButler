from fastapi import APIRouter, Depends
from apps.system.models.db import Role, Dept
from apps.system.models import request, response
from apps.account.depends import NeedAuthorization
from common.utils import get_instance, construct_tree
from fastapi_pagination import Page, Params
from http import HTTPStatus
from fastapi_pagination.ext.tortoise import paginate

router = APIRouter(
    prefix="/depts",
    tags=["部门管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("", summary="部门列表", response_model=Page[response.QueryDeptOut])
async def depts(user: NeedAuthorization, parent_id: int | None = None):
    """部门列表"""
    query_sets = Dept.filter(parent=parent_id)
    output = await paginate(query_sets)
    # 在分页结果中修改child
    for obj in output.items:
        hava_child = bool(await Dept.filter(parent=obj.id))
        obj.child = hava_child
    return output


@router.get("/full-tree", summary="部门树", response_model=list[response.QueryDeptTreeOut])
async def dept_tree(user: NeedAuthorization, params=Depends(Params)):
    """完整菜单树"""
    query_sets = await Dept.all().prefetch_related("parent")
    tree = construct_tree(query_sets)
    output = []
    for obj in tree:
        result = dict(await response.QueryDeptTreeOut.from_tortoise_orm(obj))
        output.append(result)
    return output


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


@router.post("", summary="创建部门", response_model=response.DeptDetailOut, status_code=HTTPStatus.CREATED)
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
    instance = await get_instance(Dept, pk)
    await Role.filter(id=instance.id).update(**items.model_dump())
    instance = await Dept.get(id=pk)
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


@router.delete("/{pk}", summary="删除角色")
async def delete_dept(pk: int, user: NeedAuthorization):
    """删除部门"""
    instance = await get_instance(Dept, pk)
    await instance.delete()
    return
