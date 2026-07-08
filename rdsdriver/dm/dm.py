# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

from dmPython import Connection as _Connection
from dmPython import Cursor as _Cursor


rename_kw = {
    "autocommit": "autoCommit",
    "database": "schema",
    "read_timeout": "connection_timeout",
    "write_timeout": "connection_timeout",
    "connect_timeout": "login_timeout",
}

avaliable_kw = {
    "user",
    "password",
    "host",
    "port",
    "schema",
    "connection_timeout",
    "cursorclass",
    "autoCommit",
}


class DM8Connection:
    def __init__(self, *args, **kwargs):
        keys = list(kwargs.keys())
        for k in keys:
            if k not in avaliable_kw:
                if k in rename_kw:
                    kwargs[rename_kw[k]] = kwargs[k]
                del kwargs[k]

        if "autoCommit" not in kwargs:
            kwargs["autoCommit"] = False

        if "host" in kwargs and "," in kwargs["host"]:
            kwargs["host"] = "DM"

        self._args = args
        self._kwargs = kwargs
        self._conn = _Connection(*args, **kwargs)

    def __getattr__(self, __name: str):
        return self._conn.__getattribute__(__name)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._conn.close()

    def cursor(self):
        dmCursor = self._conn.cursor()
        return DM8Cursor(dmCursor)


class DM8Cursor:
    def __init__(self, dmCursor: _Cursor):
        self._cursor = dmCursor

    def __getattr__(self, __name: str):
        return self._cursor.__getattribute__(__name)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._cursor.close()

    def modify_query(self, query) -> str:
        r = []
        i = 0
        while i < len(query):
            if query[i : i + 2] == "%s":
                r.append("?")
                i += 2
            elif query[i : i + 2] == "%%":
                r.append("%%")
                i += 2
            elif query[i] == "`":
                r.append('"')
                i += 1
            else:
                r.append(query[i])
                i += 1
        return "".join(r).replace("ESCAPE '\\\\'", "ESCAPE '\\'")

    def execute(self, query, args=None) -> int:
        query = self.modify_query(query)
        return self._cursor.execute(query, args)

    def executemany(self, query, args=None) -> int:
        query = self.modify_query(query)
        return self._cursor.executemany(query, args)


rowid_dict = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "a": 26,
    "b": 27,
    "c": 28,
    "d": 29,
    "e": 30,
    "f": 31,
    "g": 32,
    "h": 33,
    "i": 34,
    "j": 35,
    "k": 36,
    "l": 37,
    "m": 38,
    "n": 39,
    "o": 40,
    "p": 41,
    "q": 42,
    "r": 43,
    "s": 44,
    "t": 45,
    "u": 46,
    "v": 47,
    "w": 48,
    "x": 49,
    "y": 50,
    "z": 51,
    "0": 52,
    "1": 53,
    "2": 54,
    "3": 55,
    "4": 56,
    "5": 57,
    "6": 58,
    "7": 59,
    "8": 60,
    "9": 61,
    "+": 62,
    "/": 63,
}


def process_last_row_id(last_row_id):
    if isinstance(last_row_id, str):
        s = 0
        for x in last_row_id:
            s = s * 64 + rowid_dict[x]
        return s
    return last_row_id
