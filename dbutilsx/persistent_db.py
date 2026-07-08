from .dbutils.persistent_db import PersistentDB as persistentDB


class PersistentDBInfo:
    def __init__(
        self,
        creator,
        maxusage=None,
        setsession=None,
        failures=None,
        ping=1,
        closeable=False,
        threadlocal=None,
        *args,
        **kwargs,
    ):
        """Persistent DB Setting.

        creator: either an arbitrary function returning new DB-API 2
            connection objects or a DB-API 2 compliant database module
        maxusage: maximum number of reuses of a single connection
            (number of database operations, 0 or None means unlimited)
            Whenever the limit is reached, the connection will be reset.
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        failures: an optional exception class or a tuple of exception classes
            for which the connection failover mechanism shall be applied,
            if the default (OperationalError, InternalError) is not adequate
        ping: determines when the connection should be checked with ping()
            (0 = None = never, 1 = default = whenever it is requested,
            2 = when a cursor is created, 4 = when a query is executed,
            7 = always, and all other bit combinations of these values)
        closeable: if this is set to true, then closing connections will
            be allowed, but by default this will be silently ignored
        threadlocal: an optional class for representing thread-local data
            that will be used instead of our Python implementation
            (threading.local is faster, but cannot be used in all cases)
        args, kwargs: the parameters that shall be passed to the creator
            function or the connection constructor of the DB-API 2 module
        """
        self.creator = creator
        self.maxusage = maxusage
        self.setsession = setsession
        self.failures = failures
        self.ping = ping
        self.closeable = closeable
        self.threadlocal = threadlocal
        self.args = args
        self.kwargs = kwargs


class PersistentDB:
    def __init__(self, master, backup):
        """Set up the DB-API 2 connection pool.

        :param master: master db pool info.
        :type master: PersistentDBInfo

        :param backup: backup db pool info.
        :type backup: PersistentDBInfo
        """
        assert isinstance(master, PersistentDBInfo)
        assert isinstance(backup, PersistentDBInfo)
        self.writer = persistentDB(
            master.creator,
            master.maxusage,
            master.setsession,
            master.failures,
            master.ping,
            master.closeable,
            master.threadlocal,
            *master.args,
            **master.kwargs,
        )
        self.reader = persistentDB(
            backup.creator,
            backup.maxusage,
            backup.setsession,
            backup.failures,
            backup.ping,
            backup.closeable,
            backup.threadlocal,
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

    def connection(self, shareable=False):
        """Get a steady, cached DB-API 2 connection from the pool.

        If shareable is set and the underlying DB-API 2 allows it,
        then the connection may be shared with other threads.
        """
        return self.writer.connection()

    def close(self):
        """Close all connections in the pool."""
        self.reader.close()
        self.writer.close()
