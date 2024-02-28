"""
项目Enum
"""
import enum


class APIMethodEnum(str, enum.Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class DataScopeEnum(enum.IntEnum):
    ONLY_SELF = 0
    ONLY_DEPARTMENT = 1
    SELF_AND_SUBORDINATES = 2
    CUSTOM = 3
    ALL = 4

    @classmethod
    def get_display(cls, key):
        d = {
            0: "仅本人数据权限",
            1: "本部门数据权限",
            2: "本部门及以下数据权限",
            3: "自定数据权限",
            4: "全部数据权限",
        }
        return d[key]


class MenuGenreEnum(str, enum.Enum):
    """菜单类型"""

    DIRECTORY = "DIRECTORY"
    PAGE = "PAGE"
    BUTTON = "BUTTON"

    @classmethod
    def get_display(cls, key):
        d = {
            "DIRECTORY": "目录",
            "PAGE": "页面",
            "BUTTON": "按钮",
        }
        return d[key]

