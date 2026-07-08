# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
RDS统一驱动封装层
提供统一的数据库连接接口，内部根据db_type创建不同的driver实例
使用面向对象的方式，创建明确的driver类结构
"""

import logging
import os

from rdsdriver.mysql.driver import MySQLDriver
from rdsdriver.dm.driver import DM8Driver
from rdsdriver.kingbase.driver import KDB9Driver


DEFAULT_DB_TYPE = "MYSQL"

logger = logging.getLogger(__name__)


class DriverFactory:
    """驱动工厂类，负责创建对应的驱动实例"""

    _drivers = {
        "MARIADB": MySQLDriver,
        "MYSQL": MySQLDriver,
        "DM8": DM8Driver,
        "KDB9": KDB9Driver,
    }

    @classmethod
    def create_driver(cls, db_type: str):
        """根据数据库类型创建驱动实例"""
        driver_class = cls._drivers.get(db_type, None)
        if driver_class is None:
            logger.error(
                f"Unsupported database type: {db_type}, return default {DEFAULT_DB_TYPE}"
            )
            driver_class = cls._drivers.get(DEFAULT_DB_TYPE, None)
        return driver_class()


# 统一的连接函数 - 明确的实现
def connect(*args, **kwargs):
    """
    统一的数据库连接函数
    Args:
        *args: 位置参数，传递给具体驱动的connect函数
        **kwargs: 关键字参数，传递给具体驱动的connect函数
    Returns:
        数据库连接对象
    Raises:
        RuntimeError: 当连接失败时
    """

    db_type = os.environ.get("DB_TYPE", DEFAULT_DB_TYPE).upper()
    if "DB_TYPE" in kwargs:
        db_type = kwargs["DB_TYPE"].upper()
        del kwargs["DB_TYPE"]
    _driver_instance = DriverFactory.create_driver(db_type)
    return _driver_instance.connect(*args, **kwargs)
