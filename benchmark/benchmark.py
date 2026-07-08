# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import os
import time
import sys
import configparser
from multiprocessing import Queue, Process

import pymysql
from tqdm import tqdm

from dbutilsx.pooled_db import PooledDB, PooledDBInfo


def prepare(host, port, user, password, database, size):
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=True,
    )
    with connection.cursor() as cursor:
        cursor.execute("create table if not exists t1(id int)")
        cursor.execute("truncate table t1")
        args = ((1,),) * size
        cursor.executemany("insert into t1 values(%s);", args)


def run(
    op,
    c,
):
    pbar = tqdm(total=c)
    pbar.set_description(f" Child process({os.getpid()}) ")
    update = lambda *args: pbar.update()
    for i in range(c):
        op.queryAndFetchAll("select id from t1 limit 1")
        update()


if __name__ == "__main__":
    filename = "benchmark.conf"
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print(f"python {sys.argv[0]} <CONF>(default:benchmark.conf)")
    cnf = configparser.ConfigParser()
    cnf.read(filename)
    master = {k[0]: cnf.get("master", k[0]) for k in cnf.items("master")}
    backup = {k[0]: cnf.get("backup", k[0]) for k in cnf.items("backup")}
    common = {k[0]: cnf.get("common", k[0]) for k in cnf.items("common")}

    print(f"Prepare {int(common['tablesize'])} rows data start...")
    prepare(
        master["host"],
        int(master["port"]),
        master["user"],
        master["password"],
        common["database"],
        int(common["tablesize"]),
    )
    print(f"Prepare {int(common['tablesize'])} rows data end...")

    w = PooledDBInfo(
        creator=pymysql,
        host=master["host"],
        port=int(master["port"]),
        user=master["user"],
        password=master["password"],
        database=common["database"],
        autocommit=True,
    )
    r = PooledDBInfo(
        creator=pymysql,
        host=backup["host"],
        port=int(backup["port"]),
        user=backup["user"],
        password=backup["password"],
        database=common["database"],
        autocommit=True,
    )
    op = PooledDB(
        master=w,
        backup=r,
    )

    print(
        f"Run test(tablesize: {int(common['tablesize'])}, ProcessCount: {int(common['processcount'])}, ExecCount: {int(common['execcount'])}) start..."
    )

    processList = [
        Process(target=run, args=(op, int(common["execcount"])))
        for p in range(int(common["processcount"]))
    ]
    start = time.time()
    for p in processList:
        p.start()
    for p in processList:
        p.join()
    end = time.time()

    print(
        f"Run test(tablesize: {int(common['tablesize'])}, ProcessCount: {int(common['processcount'])}, ExecCount: {int(common['execcount'])}) end..."
    )

    print("*************\n")
    print(
        f"\033[1;32;40mQPS: {int(common['execcount']) * int(common['processcount']) / (end - start)}\033[0m"
    )
