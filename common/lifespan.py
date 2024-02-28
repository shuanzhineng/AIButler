from contextlib import asynccontextmanager

from loguru import logger
from tortoise import Tortoise, connections
from common.logger import init_logging
from common.db_signal import registration_db_signal
from conf.settings import AERICH_TORTOISE_ORM_CONFIG, settings

from typing_extensions import TypedDict


class FakeModel:
    @staticmethod
    def predict():
        return 1


class MlModel(TypedDict):
    fake_model: FakeModel | None


ml_models: MlModel = {"fake_model": None}


@asynccontextmanager
async def lifespan(_):
    """
    新版本fastapi使用该方式替代startup 和shutdown 事件
    https://fastapi.tiangolo.com/advanced/events/
    如果需要初始化模型等操作应该在此方法的yield前进行并在yield后释放
    """
    # startup
    init_logging()
    logger.info("项启动信号接收成功!")
    ml_models["fake_model"] = FakeModel()
    if settings.DB_URL:
        # 初始化tortoise-orm
        await Tortoise.init(config=AERICH_TORTOISE_ORM_CONFIG)
        registration_db_signal()
    yield
    # shutdown
    logger.info("项目终止信号接收成功!")
    if settings.DB_URL:
        # 关闭所有tortoise-orm连接
        await connections.close_all()
