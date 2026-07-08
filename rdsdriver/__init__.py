# -*- coding: utf-8 -*-
"""
RDS统一驱动封装层
提供统一的数据库连接接口，内部根据db_type创建不同的driver实例
遵循DB-API 2.0规范
"""

import os
import sys

from .rds_driver import *
from .cursors import *


# 创建动态访问函数
def __getattr__(name):
    _modules = {
        "MARIADB": "rdsdriver.mysql",
        "MYSQL": "rdsdriver.mysql",
        "DM8": "rdsdriver.dm",
        "KDB9": "rdsdriver.kingbase",
    }

    """动态获取cursor类"""
    db_type = os.environ.get("DB_TYPE", DEFAULT_DB_TYPE).upper()
    if name == "DictCursor":
        return DictCursorFactory.get_cursor_class(db_type)
    elif name == "TupleCursor":
        return TupleCursorFactory.get_cursor_class(db_type)
    else:
        module_path = _modules.get(db_type, None)
        if module_path is None:
            logger.error(
                f"Unsupported database type: {db_type}, return default {DEFAULT_DB_TYPE}"
            )
            module_path = _modules.get(DEFAULT_DB_TYPE, None)
        module = __import__(module_path, fromlist=[name])
        attr = getattr(module, name)
        if attr is None:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
        else:
            setattr(sys.modules[__name__], name, attr)
            return attr
