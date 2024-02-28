from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `access_log` ADD `os` VARCHAR(255) NOT NULL  COMMENT '操作系统信息' DEFAULT '';
        ALTER TABLE `access_log` DROP COLUMN `use_time`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `access_log` ADD `use_time` INT NOT NULL  COMMENT '逻辑用时' DEFAULT 0;
        ALTER TABLE `access_log` DROP COLUMN `os`;"""
