# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
DB-API 2.0 兼容性测试
验证rdsdriver模块是否符合DB-API 2.0规范
"""

import logging
import os
import sys
import time

logging.basicConfig(level=logging.DEBUG)

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import rdsdriver


os.environ["DB_TYPE"] = "DM8"

DB_CONFIG = {
    "HOST": "localhost",
    "PORT": 5236,
    "USER": "test",
    "PWD": "testpwd",
    "DB": "TESTDB",
}


def test_compatibility():
    """测试DB-API 2.0合规性"""
    print("🔍 开始DB-API 2.0合规性测试...")

    # 测试全局属性
    print("\n📋 测试全局属性:")

    # 测试必需的全局属性
    assert hasattr(rdsdriver, "apilevel"), "缺少apilevel属性"
    assert rdsdriver.apilevel == "2.0", (
        f"apilevel应该是'2.0', 实际是'{rdsdriver.apilevel}'"
    )
    print(f"  ✅ apilevel: {rdsdriver.apilevel}")

    assert hasattr(rdsdriver, "threadsafety"), "缺少threadsafety属性"
    assert rdsdriver.threadsafety in [0, 1, 2, 3], f"threadsafety应该是0-3之间的整数"
    print(f"  ✅ threadsafety: {rdsdriver.threadsafety}")

    assert hasattr(rdsdriver, "paramstyle"), "缺少paramstyle属性"
    assert rdsdriver.paramstyle in [
        "qmark",
        "numeric",
        "named",
        "format",
        "pyformat",
    ], f"paramstyle值无效"
    print(f"  ✅ paramstyle: {rdsdriver.paramstyle}")

    # 测试异常层次结构
    assert hasattr(rdsdriver, "Error"), "缺少Error异常类"
    assert hasattr(rdsdriver, "Warning"), "缺少Warning异常类"
    assert hasattr(rdsdriver, "InterfaceError"), "缺少InterfaceError异常类"
    assert hasattr(rdsdriver, "DatabaseError"), "缺少DatabaseError异常类"
    assert hasattr(rdsdriver, "DataError"), "缺少DataError异常类"
    assert hasattr(rdsdriver, "OperationalError"), "缺少OperationalError异常类"
    assert hasattr(rdsdriver, "IntegrityError"), "缺少IntegrityError异常类"
    assert hasattr(rdsdriver, "InternalError"), "缺少InternalError异常类"
    assert hasattr(rdsdriver, "ProgrammingError"), "缺少ProgrammingError异常类"
    assert hasattr(rdsdriver, "NotSupportedError"), "缺少NotSupportedError异常类"
    print("  ✅ 异常层次结构完整")

    # 测试类型对象
    assert hasattr(rdsdriver, "STRING"), "缺少STRING类型"
    assert hasattr(rdsdriver, "BINARY"), "缺少BINARY类型"
    assert hasattr(rdsdriver, "NUMBER"), "缺少NUMBER类型"
    assert hasattr(rdsdriver, "DATETIME"), "缺少DATETIME类型"
    assert hasattr(rdsdriver, "ROWID"), "缺少ROWID类型"
    print("  ✅ 类型对象完整")

    # 测试构造函数
    assert hasattr(rdsdriver, "Date"), "缺少Date构造函数"
    assert hasattr(rdsdriver, "Time"), "缺少Time构造函数"
    assert hasattr(rdsdriver, "Timestamp"), "缺少Timestamp构造函数"
    assert hasattr(rdsdriver, "DateFromTicks"), "缺少DateFromTicks构造函数"
    assert hasattr(rdsdriver, "TimeFromTicks"), "缺少TimeFromTicks构造函数"
    assert hasattr(rdsdriver, "TimestampFromTicks"), "缺少TimestampFromTicks构造函数"

    date_obj = rdsdriver.Date(2023, 12, 25)
    print(f"  ✅ Date构造函数: {date_obj}")

    time_obj = rdsdriver.Time(14, 30, 45)
    print(f"  ✅ Time构造函数: {time_obj}")

    timestamp_obj = rdsdriver.Timestamp(2023, 12, 25, 14, 30, 45)
    print(f"  ✅ Timestamp构造函数: {timestamp_obj}")

    # 测试Ticks构造函数
    current_ticks = time.time()

    date_from_ticks = rdsdriver.DateFromTicks(current_ticks)
    print(f"  ✅ DateFromTicks构造函数: {date_from_ticks}")

    time_from_ticks = rdsdriver.TimeFromTicks(current_ticks)
    print(f"  ✅ TimeFromTicks构造函数: {time_from_ticks}")

    timestamp_from_ticks = rdsdriver.TimestampFromTicks(current_ticks)
    print(f"  ✅ TimestampFromTicks构造函数: {timestamp_from_ticks}")

    print("  ✅ 构造函数完整")

    # 测试连接函数
    assert hasattr(rdsdriver, "connect"), "缺少connect函数"
    print("  ✅ connect函数存在")


def test_conn():
    conn = rdsdriver.connect(
        host=DB_CONFIG["HOST"],
        port=DB_CONFIG["PORT"],
        user=DB_CONFIG["USER"],
        password=DB_CONFIG["PWD"],
        autocommit=True,
    )

    # Connection
    assert hasattr(conn, "close")
    assert hasattr(conn, "commit")
    assert hasattr(conn, "rollback")
    assert hasattr(conn, "cursor")

    # Cursor
    cursor = conn.cursor()
    assert hasattr(cursor, "description")
    assert hasattr(cursor, "rowcount")
    assert hasattr(cursor, "arraysize")
    assert hasattr(cursor, "callproc")
    assert hasattr(cursor, "close")
    assert hasattr(cursor, "execute")
    assert hasattr(cursor, "executemany")
    assert hasattr(cursor, "fetchone")
    assert hasattr(cursor, "fetchmany")
    assert hasattr(cursor, "fetchall")
    assert hasattr(cursor, "setinputsizes")
    assert hasattr(cursor, "setoutputsize")
    cursor.close()
    conn.close()


def test_init():
    conn = rdsdriver.connect(
        host=DB_CONFIG["HOST"],
        port=DB_CONFIG["PORT"],
        user=DB_CONFIG["USER"],
        password=DB_CONFIG["PWD"],
        autocommit=True,
    )
    cursor = conn.cursor()
    rslt = cursor.execute(f"CREATE SCHEMA {DB_CONFIG['DB']}")
    cursor.close()
    conn.close()


def test_table_opr():
    conn = rdsdriver.connect(
        host=DB_CONFIG["HOST"],
        port=DB_CONFIG["PORT"],
        user=DB_CONFIG["USER"],
        password=DB_CONFIG["PWD"],
        database=DB_CONFIG["DB"],
        autocommit=True,
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS t1")
    cursor.execute("CREATE TABLE IF NOT EXISTS t1(id int)")
    cursor.executemany("INSERT INTO t1 VALUES(%s)", ((1,), (2,), (3,), (4,)))
    cursor.execute("SELECT * FROM t1")
    r = cursor.fetchall()
    assert len(r) == 4

    cursor.execute("DELETE FROM t1")
    cursor.execute("SELECT * FROM t1")
    r = cursor.fetchall()
    assert len(r) == 0

    cursor.close()
    conn.close()


def test_cursor():
    for cursorclass in [rdsdriver.DictCursor, rdsdriver.TupleCursor]:
        conn = rdsdriver.connect(
            host=DB_CONFIG["HOST"],
            port=DB_CONFIG["PORT"],
            user=DB_CONFIG["USER"],
            password=DB_CONFIG["PWD"],
            database=DB_CONFIG["DB"],
            autocommit=True,
            cursorclass=cursorclass,
        )

        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS t1")
        cursor.execute("CREATE TABLE IF NOT EXISTS t1(id int)")
        cursor.executemany("INSERT INTO t1 VALUES(%s)", ((1,), (2,), (3,), (4,)))
        cursor.execute("SELECT * FROM t1")
        r = cursor.fetchall()
        assert len(r) == 4
        cursor.close()
        conn.close()


def test_with():
    with rdsdriver.connect(
        host=DB_CONFIG["HOST"],
        port=DB_CONFIG["PORT"],
        user=DB_CONFIG["USER"],
        password=DB_CONFIG["PWD"],
        database=DB_CONFIG["DB"],
        autocommit=True,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS t1")
            cursor.execute("CREATE TABLE IF NOT EXISTS t1(id int)")
            cursor.executemany("INSERT INTO t1 VALUES(%s)", ((1,), (2,), (3,), (4,)))
            cursor.execute("SELECT * FROM `t1`")
            r = cursor.fetchall()
            assert len(r) == 4


if __name__ == "__main__":
    test_compatibility()
    test_conn()
    test_init()
    test_table_opr()
    test_cursor()
    test_with()
