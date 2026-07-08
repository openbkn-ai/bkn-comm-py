# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
定义统一的游标接口，包括字典游标和元组游标
"""

import logging

from rdsdriver.mysql.cursors import MySQLDictCursor, MySQLTupleCursor
from rdsdriver.dm.cursors import DM8DictCursor, DM8TupleCursor
from rdsdriver.kingbase.cursors import KDB9DictCursor, KDB9TupleCursor


DEFAULT_DB_TYPE = "MYSQL"

logger = logging.getLogger(__name__)


class DictCursorFactory:
    """字典游标工厂类，负责创建对应的游标实例"""

    _cursor_classes = {
        "MARIADB": MySQLDictCursor,
        "MYSQL": MySQLDictCursor,
        "DM8": DM8DictCursor,
        "KDB9": KDB9DictCursor,
    }

    @classmethod
    def get_cursor_class(cls, db_type: str):
        """根据数据库类型创建游标实例"""
        cursor_class = cls._cursor_classes.get(db_type, None)
        if cursor_class is None:
            logger.error(
                f"Unsupported database type: {db_type}, return default {DEFAULT_DB_TYPE}"
            )
            cursor_class = cls._cursor_classes.get(DEFAULT_DB_TYPE, None)
        return cursor_class


class TupleCursorFactory:
    """元组游标工厂类，负责创建对应的游标实例"""

    _cursor_classes = {
        "MARIADB": MySQLTupleCursor,
        "MYSQL": MySQLTupleCursor,
        "DM8": DM8TupleCursor,
        "KDB9": KDB9TupleCursor,
    }

    @classmethod
    def get_cursor_class(cls, db_type: str):
        """根据数据库类型创建游标实例"""
        cursor_class = cls._cursor_classes.get(db_type, None)
        if cursor_class is None:
            logger.error(
                f"Unsupported database type: {db_type}, return default {DEFAULT_DB_TYPE}"
            )
            cursor_class = cls._cursor_classes.get(DEFAULT_DB_TYPE, None)
        return cursor_class
