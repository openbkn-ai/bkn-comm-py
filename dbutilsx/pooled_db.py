# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

from .dbutils.pooled_db import PooledDB as pooledDB


class PooledDBInfo:
    def __init__(
        self,
        creator,
        mincached=0,
        maxcached=0,
        maxshared=0,
        maxconnections=0,
        blocking=False,
        maxusage=None,
        setsession=None,
        reset=True,
        failures=None,
        ping=1,
        *args,
        **kwargs,
    ):
        """Pooled DB Setting.

        creator: either an arbitrary function returning new DB-API 2
            connection objects or a DB-API 2 compliant database module
        mincached: initial number of idle connections in the pool
            (0 means no connections are made at startup)
        maxcached: maximum number of idle connections in the pool
            (0 or None means unlimited pool size)
        maxshared: maximum number of shared connections
            (0 or None means all connections are dedicated)
            When this maximum number is reached, connections are
            shared if they have been requested as shareable.
        maxconnections: maximum number of connections generally allowed
            (0 or None means an arbitrary number of connections)
        blocking: determines behavior when exceeding the maximum
            (if this is set to true, block and wait until the number of
            connections decreases, otherwise an error will be reported)
        maxusage: maximum number of reuses of a single connection
            (0 or None means unlimited reuse)
            When this maximum usage number of the connection is reached,
            the connection is automatically reset (closed and reopened).
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        reset: how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        failures: an optional exception class or a tuple of exception classes
            for which the connection failover mechanism shall be applied,
            if the default (OperationalError, InternalError) is not adequate
        ping: determines when the connection should be checked with ping()
            (0 = None = never, 1 = default = whenever fetched from the pool,
            2 = when a cursor is created, 4 = when a query is executed,
            7 = always, and all other bit combinations of these values)
        args, kwargs: the parameters that shall be passed to the creator
            function or the connection constructor of the DB-API 2 module
        """
        self.creator = creator
        self.mincached = mincached
        self.maxcached = maxcached
        self.maxshared = maxshared
        self.maxconnections = maxconnections
        self.blocking = blocking
        self.maxusage = maxusage
        self.setsession = setsession
        self.reset = reset
        self.failures = failures
        self.ping = ping
        self.args = args
        self.kwargs = kwargs


class PooledDB:
    def __init__(self, master, backup):
        """Set up the DB-API 2 connection pool.

        :param master: master db pool info.
        :type master: PooledDBInfo

        :param backup: backup db pool info.
        :type backup: PooledDBInfo
        """
        assert isinstance(master, PooledDBInfo)
        assert isinstance(backup, PooledDBInfo)
        self.writer = pooledDB(
            master.creator,
            master.mincached,
            master.maxcached,
            master.maxshared,
            master.maxconnections,
            master.blocking,
            master.maxusage,
            master.setsession,
            master.reset,
            master.failures,
            master.ping,
            *master.args,
            **master.kwargs,
        )
        self.reader = pooledDB(
            backup.creator,
            backup.mincached,
            backup.maxcached,
            backup.maxshared,
            backup.maxconnections,
            backup.blocking,
            backup.maxusage,
            backup.setsession,
            backup.reset,
            backup.failures,
            backup.ping,
            *backup.args,
            **backup.kwargs,
        )

    def __del__(self):
        """Delete the pool."""
        try:
            self.close()
        except:
            pass

    def queryAndFetchOne(self, query, args=None):
        """Exec a query on backup node and fetch one row.

        :param query: Query to execute.
        :type query: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Query result.
        :rtype: tuple
        """
        with self.reader.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.fetchone()

    def queryAndFetchMany(self, query, args=None, size=None):
        """Exec a query on backup node and Fetch several rows

        :param query: Query to execute.
        :type query: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :param size: Return Row size. (optional)
        :type args: int

        :return: Query results.
        :rtype: tuple

        """
        with self.reader.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.fetchmany(size)

    def queryAndFetchAll(self, query, args=None):
        """Exec a query on backup node and Fetch all rows

        :param query: Query to execute.
        :type query: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Query results.
        :rtype: tuple

        """
        with self.reader.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.fetchall()

    def execute(self, query, args=None):
        """Execute a query on master node.

        :param query: Query to execute.
        :type query: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows.
        :rtype: int
        """
        with self.writer.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.rowcount

    def executemany(self, query, args):
        """Run several data against one query on master node.

        :param query: Query to execute.
        :type query: str

        :param args: Sequence of sequences or mappings. It is used as parameter.
        :type args: tuple or list

        :return: Number of rows affected, if any.
        :rtype: int or None

        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        with self.writer.connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, args)
                return cur.rowcount

    def connection(self, shareable=True):
        """Get a steady, cached DB-API 2 connection from the pool.

        If shareable is set and the underlying DB-API 2 allows it,
        then the connection may be shared with other threads.
        """
        return self.writer.connection(shareable)

    def close(self):
        """Close all connections in the pool."""
        try:
            self.reader.close()
        except:
            pass
        try:
            self.writer.close()
        except:
            pass
