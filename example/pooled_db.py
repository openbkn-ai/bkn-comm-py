import pymysql
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

if __name__ == "__main__":
    w = PooledDBInfo(
        creator=pymysql,
        mincached=1,
        maxcached=5,
        maxshared=1,
        maxconnections=20,
        blocking=False,
        maxusage=None,
        setsession=None,
        reset=True,
        failures=None,
        ping=1,
        host="localhost",
        port=3308,
        user="test",
        password="testpwd",
        database="testdb",
        autocommit=True,
    )
    r = w
    op = PooledDB(
        master=w,
        backup=r,
    )
    op.execute("create table if not exists t1(id int)")
    op.executemany("replace into t1 values(%s);", ((1,), (2,), (3,)))
    print(op.queryAndFetchMany("select * from t1", size=2))
    print(op.queryAndFetchAll("select * from t1"))

    # DB API 2.0 Connection Object
    with op.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("delete from t1")
            print(cur.rowcount)
