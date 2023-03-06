import mariadb
from .models import *
import typing as t


DBError = mariadb.Error
DBIntegrityError = mariadb.IntegrityError
DBOperationalError = mariadb.OperationalError
DBProgrammingError = mariadb.ProgrammingError
DBInterfaceError = mariadb.InterfaceError
DBInternalError = mariadb.InternalError

DBConnection = mariadb.Connection
DBCursor = mariadb.Cursor


ModelError = DBIntegrityError


class DefaultModelError(ModelError):
    def __init__(self, error: DBIntegrityError):
        super().__init__(f"Unexpected database error: {error}.")


global __connection
__connection: DBConnection


def get_db(**config) -> DBCursor:
    global __connection
    __connection = mariadb.connect(**config)
    if not isinstance(__connection, DBConnection):
        raise DBError(f"Failed to connect to database with configuration:\n{config}")
    return __connection.cursor()


def commit_db(db: DBCursor) -> None:  # pyright: ignore
    __connection.commit()


def close_db(db: DBCursor) -> None:  # pyright: ignore
    __connection.close()


def db_execute(
    db: DBCursor, statement: str, params: tuple = (), **kwargs
) -> t.Sequence:
    try:
        db.execute(statement, params, **kwargs)
    except (
        DBOperationalError,
        DBProgrammingError,
        DBInterfaceError,
        DBInternalError,
    ) as error:
        raise DBError(f'Database usage error: "{error}".')

    try:
        return db.fetchall()
    except DBError:
        return ()


def db_executemany(
    db: DBCursor, statement: str, params_tuples: t.Sequence[tuple] = (), **kwargs
) -> None:
    try:
        db.executemany(statement, params_tuples, **kwargs)
    except (
        DBOperationalError,
        DBProgrammingError,
        DBInterfaceError,
        DBInternalError,
    ) as error:
        raise DBError(f'Database usage error: "{error}".')


def db_callproc(
    db: DBCursor, procedure: str, params: tuple = (), **kwargs
) -> t.Sequence:
    try:
        out_args = db.callproc(procedure, params, **kwargs)
        if isinstance(out_args, dict):
            return tuple(out_args.values())
        if isinstance(out_args, tuple):
            return out_args
    except (
        DBOperationalError,
        DBProgrammingError,
        DBInterfaceError,
        DBInternalError,
    ) as error:
        raise DBError(f'Database usage error: "{error}".')

    return ()


class DBCursorContext:
    def __init__(self, config: dict[str, t.Any]):
        self.config = config

    def __enter__(self):
        self.cursor = get_db(**self.config)
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        commit_db(self.cursor)
        self.cursor.close()

