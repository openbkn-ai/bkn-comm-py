# -*- coding: utf-8 -*-
"""
MySQL驱动实现
"""

import logging


logger = logging.getLogger(__name__)


class MySQLDriver:
    """MySQL驱动封装"""

    def connect(self, *args, **kwargs):
        """连接MySQL数据库"""
        try:
            from . import mysql as driver_module

            return driver_module.EnhancedConnection(*args, **kwargs)
        except ImportError as e:
            logger.error(f"Failed to load MySQL driver: {e}")
            raise
