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


class LabelTaskStatusEnum(str, enum.Enum):
    """数据质检状态"""

    DRAFT = "DRAFT"
    IMPORTED = "IMPORTED"
    CONFIGURED = "CONFIGURED"
    INPROGRESS = "INPROGRESS"
    FINISHED = "FINISHED"

    @classmethod
    def get_display(cls, key):
        d = {
            "DRAFT": "初始化",
            "IMPORTED": "已导入",
            "CONFIGURED": "已配置",
            "INPROGRESS": "进行中",
            "FINISHED": "已完成",
        }
        return d[key]


class MediaTypeEnum(str, enum.Enum):
    """标注任务媒体类型"""

    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"

    @classmethod
    def get_display(cls, key):
        d = {
            "IMAGE": "图片",
            "VIDEO": "视频",
            "AUDIO": "音频",
        }
        return d[key]


class LabelTaskSampleStateEnum(str, enum.Enum):
    """标注任务样例状态"""

    NEW = "NEW"
    SKIPPED = "SKIPPED"
    DONE = "DONE"

    @classmethod
    def get_display(cls, key):
        d = {
            "NEW": "未标注",
            "SKIPPED": "跳过",
            "DONE": "已标注",
        }
        return d[key]


class AnnotationTypeEnum(str, enum.Enum):
    """
    标注类型
    """

    IMAGE_CLASSIFY = "IMAGE_CLASSIFY"  # 图像分类
    OBJECT_DETECTION = "OBJECT_DETECTION"  # 物体检测

    @classmethod
    def get_display(cls, key):
        d = {
            "IMAGE_CLASSIFY": "图像分类",
            "OBJECT_DETECTION": "物体检测",
        }
        return d[key]


class TrainStatusEnum(str, enum.Enum):
    """
    训练状态
    """

    WAITING = "WAITING"
    TRAINING = "TRAINING"
    FAILURE = "FAILURE"
    FINISH = "FINISH"

    @classmethod
    def get_display(cls, key):
        d = {
            "WAITING": "等待训练",
            "TRAINING": "训练中",
            "FAILURE": "已失败",
            "FINISH": "已完成",
        }
        return d[key]
