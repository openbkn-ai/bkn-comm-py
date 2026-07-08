# -*- coding: utf-8 -*-


def TestTime(cursor):
    tableSql = (
        "CREATE TABLE IF NOT EXISTS `test_time`("
        "`id` INT(4),"
        "`time` DATETIME DEFAULT current_timestamp(),"
        "`ts` TIMESTAMP DEFAULT current_timestamp()"
        ")"
    )
    cursor.execute(tableSql)

    os = {"id": 1}
    cursor.execute("INSERT INTO `test_time` (`id`) VALUES(%s)", [1])

    cursor.execute("SELECT `id`, `time`, `ts` FROM `test_time` WHERE id=%s", (1,))
    ns = cursor.fetchone()

    if ns["id"] != os["id"]:
        print(f"data not match: new: {ns}, org: {os}")

    ts1 = int(ns["time"].timestamp())
    ts2 = int(ns["ts"].timestamp())
    print(ts1, ts2)

    print("success")
