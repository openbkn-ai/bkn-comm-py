# -*- coding: utf-8 -*-
"""
KDB9驱动实现
"""

import logging


logger = logging.getLogger(__name__)


class KDB9Driver:
    """人大金仓9驱动封装"""

    def connect(self, *args, **kwargs):
        """连接人大金仓9数据库"""
        try:
            from . import kingbase as driver_module

            autocommit = 0
            if "autocommit" in kwargs:
                autocommit = kwargs["autocommit"]
                del kwargs["autocommit"]

            conn = driver_module.KDB9Connection(sslmode="disable", **kwargs)
            conn.set_session(autocommit=autocommit)
            return conn
        except ImportError as e:
            logger.error(f"Failed to load KDB9 driver: {e}")
            raise
