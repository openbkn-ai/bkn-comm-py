# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import sys
import os
from dbutils.pooled_db import PooledDB

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import rdsdriver
from rdsdriver import *
from kdb_time import *


DB_CONFIG_ROOT = {
    "host": "localhost",
    "user": "test",
    "password": "testpwd",
    "port": 54321,
    "autocommit": True,
}


def Test():
    try:
        os.environ["DB_TYPE"] = "kdb9"
        conn = rdsdriver.connect(
            host=DB_CONFIG_ROOT["host"],
            port=int(DB_CONFIG_ROOT["port"]),
            user=DB_CONFIG_ROOT["user"],
            password=DB_CONFIG_ROOT["password"],
            autocommit=True,
        )
        cursor = conn.cursor()
        cursor.execute("CREATE SCHEMA test1")
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)


def Test_PooledDB():
    try:
        os.environ["DB_TYPE"] = "kdb9"
        pool = PooledDB(
            mincached=0,
            maxcached=5,
            maxshared=1,
            maxconnections=20,
            blocking=False,
            maxusage=None,
            setsession=None,
            reset=True,
            failures=None,
            ping=1,
            autocommit=DB_CONFIG_ROOT["autocommit"],
            host=DB_CONFIG_ROOT["host"],
            port=DB_CONFIG_ROOT["port"],
            user=DB_CONFIG_ROOT["user"],
            password=DB_CONFIG_ROOT["password"],
            database="openbkn",
            creator=rdsdriver,
            cursorclass=rdsdriver.DictCursor,
        )

        conn = pool.connection()
        cursor = conn.cursor()

        cursor.execute("DROP SCHEMA IF EXISTS `test` CASCADE")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS `test`")
        cursor.execute("SET SEARCH_PATH TO `test`")

        TestTime(cursor)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    Test()
