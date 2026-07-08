# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import os
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import rdsdriver
from dbutilsx.persistent_db import PersistentDB, PersistentDBInfo
from dbutilsx.pooled_db import PooledDB, PooledDBInfo


DB_CONFIGS = {
    "MYSQL": {
        "HOST": "localhost",
        "PORT": 3307,
        "USER": "test",
        "PWD": "testpwd",
        "DB": "TESTDB",
    },
    "DM8": {
        "HOST": "localhost",
        "PORT": 5236,
        "USER": "test",
        "PWD": "testpwd",
        "DB": "TESTDB",
    },
    "KDB9": {
        "HOST": "localhost",
        "PORT": 54321,
        "USER": "test",
        "PWD": "testpwd",
        "DB": "TESTDB",
    },
}


def create_dbutilsx_db(db_config, db_class_info, db_class):
    w = db_class_info(
        creator=rdsdriver,
        host=db_config["HOST"],
        port=db_config["PORT"],
        user=db_config["USER"],
        password=db_config["PWD"],
        database=db_config["DB"],
        autocommit=True,
        cursorclass=rdsdriver.TupleCursor,
    )
    op = db_class(
        master=w,
        backup=w,
    )
    return op


def test_queryAndFetchOne(op):
    op.execute("create table if not exists t1(id int)")
    op.execute("insert into t1 values(%s)", (1,))
    r = op.queryAndFetchOne("select * from t1")
    assert r == (1,)
    op.execute("delete from t1")


def test_queryAndFetchMany(op):
    op.execute("create table if not exists t1(id int)")
    op.executemany("insert into t1 values(%s);", ((1,), (2,), (3,)))
    r = op.queryAndFetchMany("select * from t1", size=1)
    assert len(r) == 1 and r[0] == (1,)
    r = op.queryAndFetchMany("select * from t1", size=5)
    assert len(r) == 3
    op.execute("delete from t1")


def test_queryAndFetchAll(op):
    op.execute("create table if not exists t1(id int)")
    op.executemany("insert into t1 values(%s);", ((1,), (2,), (3,)))
    r = op.queryAndFetchAll("select * from t1")
    assert len(r) == 3
    op.execute("delete from t1")


def test_connection(op):
    with op.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("create table if not exists t1(id int)")
            cur.execute("insert into t1 values(%s)", (1,))
            cur.execute("select * from t1")
            r = cur.fetchone()
            assert r == (1,)
            op.execute("delete from t1")


def test_readWriteSplit(db_config, db_class_info, db_class):
    w = db_class_info(
        creator=rdsdriver,
        host=db_config["HOST"],
        port=db_config["PORT"],
        user=db_config["USER"],
        password=db_config["PWD"],
        database=db_config["DB"],
        autocommit=True,
        cursorclass=rdsdriver.TupleCursor,
    )
    r = db_class_info(
        creator=rdsdriver,
        host=db_config["HOST"],
        port=db_config["PORT"],
        user=db_config["USER"],
        password=db_config["PWD"],
        database=db_config["DB"],
        autocommit=True,
        cursorclass=rdsdriver.TupleCursor,
    )
    op = db_class(
        master=w,
        backup=r,
    )
    op.execute("create table if not exists t1(id int)")
    op.executemany("insert into t1 values(%s);", ((1,), (2,), (3,)))
    r = op.queryAndFetchAll("select * from t1")
    assert len(r) == 3
    op.execute("delete from t1")


if __name__ == "__main__":
    for db_type, db_config in DB_CONFIGS.items():
        os.environ["DB_TYPE"] = db_type

        for db_class_info, db_class in (
            (PersistentDBInfo, PersistentDB),
            (PooledDBInfo, PooledDB),
        ):
            op = create_dbutilsx_db(db_config, db_class_info, db_class)
            test_queryAndFetchOne(op)
            test_queryAndFetchMany(op)
            test_queryAndFetchAll(op)
            test_connection(op)
            test_readWriteSplit(db_config, db_class_info, db_class)
            print(f"  ✅ {db_type} {db_class.__name__} 测试通过")
