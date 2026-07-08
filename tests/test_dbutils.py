import os
import sys

from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import rdsdriver


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


def test_persistent_db(db_config):
    op = PersistentDB(
        creator=rdsdriver,
        host=db_config["HOST"],
        port=db_config["PORT"],
        user=db_config["USER"],
        password=db_config["PWD"],
        database=db_config["DB"],
        autocommit=True,
        cursorclass=rdsdriver.TupleCursor,
    )

    with op.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("create table if not exists t1(id int)")
            cur.execute("insert into t1 values(%s)", (1,))
            cur.execute("select * from t1")
            r = cur.fetchone()
            assert r == (1,)
            cur.execute("delete from t1")


def test_pooled_db(db_config):
    op = PooledDB(
        creator=rdsdriver,
        host=db_config["HOST"],
        port=db_config["PORT"],
        user=db_config["USER"],
        password=db_config["PWD"],
        database=db_config["DB"],
        autocommit=True,
        cursorclass=rdsdriver.TupleCursor,
    )

    with op.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("create table if not exists t1(id int)")
            cur.execute("insert into t1 values(%s)", (1,))
            cur.execute("select * from t1")
            r = cur.fetchone()
            assert r == (1,)
            cur.execute("delete from t1")


if __name__ == "__main__":
    for db_type, db_config in DB_CONFIGS.items():
        os.environ["DB_TYPE"] = db_type

        test_persistent_db(db_config)
        test_pooled_db(db_config)
        print(f"  ✅ {db_type} 测试通过")
