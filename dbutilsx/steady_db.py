# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

from .dbutils.steady_db import SteadyDBConnection as steadyDB


class SteadyDBInfo:
    def __init__(
        self,
        creator,
        maxusage=None,
        setsession=None,
        failures=None,
        ping=1,
        closeable=False,
        *args,
        **kwargs,
    ):
        """Steady DB Setting.

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
        args, kwargs: the parameters that shall be passed to the creator
            function or the connection constructor of the DB-API 2 module
        """
        self.creator = creator
        self.maxusage = maxusage
        self.setsession = setsession
        self.failures = failures
        self.ping = ping
        self.closeable = closeable
        self.args = args
        self.kwargs = kwargs


class SteadyDB:
    def __init__(self, master, backup):
        """Set up the DB-API 2 connection pool.

        :param master: master db info.
        :type master: SteadyDBInfo

        :param backup: backup db info.
        :type backup: SteadyDBInfo
        """
        assert isinstance(master, SteadyDBInfo)
        assert isinstance(backup, SteadyDBInfo)
        self.writer = steadyDB(
            master.creator,
            master.maxusage,
            master.setsession,
            master.failures,
            master.ping,
            master.closeable,
            *master.args,
            **master.kwargs,
        )
        self.reader = steadyDB(
            backup.creator,
            backup.maxusage,
            backup.setsession,
            backup.failures,
            backup.ping,
            backup.closeable,
            *backup.args,
            **backup.kwargs,
        )

    def __del__(self):
        """Delete the connections."""
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
                return cur.fetchmany(size) if size else cur.fetchall()

    def queryAndFetchAll(self, query, args=None):
        """Exec a query on backup node and fetch all rows.

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

    def execute(self, operation, args=None):
        """Execute a query on master node.

        :param operation: Query to execute.
        :type operation: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows.
        :rtype: int
        """
        with self.writer.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(operation, args)
                return cur.rowcount

    def executemany(self, operation, seq_of_parameters):
        """Execute multiple operations on master node.

        :param operation: Query to execute.
        :type operation: str

        :param seq_of_parameters: Sequence of parameters.
        :type seq_of_parameters: list

        :return: Number of affected rows.
        :rtype: int
        """
        with self.writer.connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(operation, seq_of_parameters)
                return cur.rowcount

    def close(self):
        """Close the connections."""
        try:
            self.writer.close()
            self.reader.close()
        except:
            pass
