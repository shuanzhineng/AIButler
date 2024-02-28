from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `access_log` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键id',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `modifier_id` BIGINT   COMMENT '修改人id',
    `dept_belong_id` BIGINT   COMMENT '数据归属部门id',
    `api` VARCHAR(255) NOT NULL  COMMENT '接口地址' DEFAULT '',
    `method` VARCHAR(255) NOT NULL  COMMENT '接口请求方法',
    `ip_address` VARCHAR(255) NOT NULL  COMMENT 'ip地址' DEFAULT '',
    `browser` VARCHAR(255) NOT NULL  COMMENT '浏览器信息' DEFAULT '',
    `http_status_code` INT NOT NULL  COMMENT 'http状态码' DEFAULT 0,
    `request_body` LONGTEXT NOT NULL  COMMENT '请求体',
    `response_body` LONGTEXT NOT NULL  COMMENT '响应体',
    `use_time` INT NOT NULL  COMMENT '逻辑用时' DEFAULT 0,
    `creator_id` BIGINT
) CHARACTER SET utf8mb4 COMMENT='访问日志';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `access_log`;"""
