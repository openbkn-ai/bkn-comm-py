# -*- coding: utf-8 -*-
"""
DM8驱动实现
"""

import logging


logger = logging.getLogger(__name__)


class DM8Driver:
    """达梦8驱动封装"""

    def connect(self, *args, **kwargs):
        """连接达梦8数据库"""
        try:
            from . import dm as driver_module

            return driver_module.DM8Connection(*args, **kwargs)
        except ImportError as e:
            logger.error(f"Failed to load DM8 driver: {e}")
            raise
