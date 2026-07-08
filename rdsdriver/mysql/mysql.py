# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import logging
from pymysql.connections import Connection as PyMySQLConnection


logger = logging.getLogger(__name__)


class EnhancedConnection(PyMySQLConnection):
    def __init__(self, *args, **kwargs):
        """
        初始化EnhancedConnection
        """
        super().__init__(*args, **kwargs)

    def ping(self, reconnect=True):
        """
        重写ping方法，添加超时保护
        """
        try:
            if self._sock is None:
                if reconnect:
                    self.connect()
                    return True
                else:
                    return False
            # 保存原有的超时设置
            old_read_timeout = self._read_timeout

            # 临时设置一个较短的超时
            self._read_timeout = 3

            try:
                with self.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                return True
            finally:
                # 恢复原有的超时设置
                self._read_timeout = old_read_timeout
        except Exception as e:
            logger.exception("openbkn rds sdk ping error %s", str(e))
            if reconnect:
                try:
                    self.connect()
                    return True
                except Exception as e:
                    logger.exception(
                        "openbkn rds sdk ping first reconnect error %s", str(e)
                    )
                    return False
            return False


def process_last_row_id(last_row_id):
    return last_row_id
