# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import pymysql
from dbutilsx.persistent_db import PersistentDB, PersistentDBInfo

if __name__ == "__main__":
    w = PersistentDBInfo(
        creator=pymysql,
        maxusage=None,
        setsession=None,
        failures=None,
        ping=1,
        closeable=False,
        threadlocal=None,
        host="localhost",
        port=3308,
        user="test",
        password="testpwd",
        database="deploy",
        autocommit=True,
    )
    r = w
    op = PersistentDB(
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
