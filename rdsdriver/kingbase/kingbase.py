# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

import ksycopg2


def bytea2bytes(value, cur):
    m = ksycopg2.BINARY(value, cur)
    if m is not None:
        return m.tobytes()


BYTEA2BYTES = ksycopg2.extensions.new_type(
    ksycopg2.BINARY.values, "BYTEA2BYTES", bytea2bytes
)
ksycopg2.extensions.register_type(BYTEA2BYTES)


def cast_kingbase_tinyint(value, cursor):
    if value is None:
        return None
    return int(value)


TINYINT_OID = 8100
tinyint_caster = ksycopg2.extensions.new_type(
    (TINYINT_OID,), "TINYINT", cast_kingbase_tinyint
)
ksycopg2.extensions.register_type(tinyint_caster)


rename_kw = {"cursorclass": "cursor_factory"}

avaliable_kw = {
    "user",
    "password",
    "host",
    "port",
    "connect_timeout",
    "autocommit",
    "database",
}


class KDB9Connection:
    def __init__(self, *args, **kwargs):
        keys = list(kwargs.keys())
        for k in keys:
            if k not in avaliable_kw:
                if k in rename_kw:
                    kwargs[rename_kw[k]] = kwargs[k]
                del kwargs[k]

        if "database" in kwargs:
            schema = kwargs["database"]
            kwargs["options"] = f"-c search_path={schema}"
        kwargs["database"] = "openbkn"
        kwargs["client_encoding"] = "utf-8"

        self._args = args
        self._kwargs = kwargs
        self._session = dict()
        self._conn = ksycopg2.connect(**kwargs)

    def __getattr__(self, __name: str):
        if __name in ("close", "commit", "rollback", "cursor"):
            return self._conn.__getattribute__(__name)
        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._conn.close()

    def set_session(self, **kwargs):
        self._session = kwargs
        if self._conn:
            self._conn.set_session(**kwargs)

    def ping(self):
        try:
            with self._conn.cursor() as c:
                c.execute("select 1")
        except Exception as e:
            self._conn = ksycopg2.connect(**self._kwargs)
            self._conn.set_session(**self._session)


def process_last_row_id(last_row_id):
    return last_row_id
