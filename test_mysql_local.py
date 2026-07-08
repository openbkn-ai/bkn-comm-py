# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
本地MySQL连接测试脚本
"""

import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DB_TYPE"] = "MYSQL"

import rdsdriver

DB_CONFIG = {
    "HOST": "0.0.0.0",
    "PORT": 2881,
    "USER": "dev_user@test",
    "PWD": "wjgl_admin@SERVICE:WJGL_JZ_YW",
}


def test_connect():
    print("正在连接数据库...")
    conn = rdsdriver.connect(
        host=DB_CONFIG["HOST"],
        port=DB_CONFIG["PORT"],
        user=DB_CONFIG["USER"],
        password=DB_CONFIG["PWD"],
        autocommit=True,
    )
    print("连接成功!")

    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("数据库列表:")
    for db in databases:
        print(f"  {db}")

    cursor.close()
    conn.close()
    print("连接已关闭.")


if __name__ == "__main__":
    test_connect()
