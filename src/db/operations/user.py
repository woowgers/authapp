from db import DBCursor, ModelError, db_execute
from db.models import *


def db_get_users(db: DBCursor) -> tuple[User]:
    SQL_QUERY = """
        SELECT user_id, email, user_type, name, pw_hash
        FROM user
    """
    return tuple(User(*user_tuple) for user_tuple in db_execute(db, SQL_QUERY))


def db_get_admins(db: DBCursor) -> tuple[User]:
    SQL_QUERY = """
        SELECT user_id, email, user_type, name, pw_hash
        FROM user
        WHERE user_type = 'admin'
    """
    return tuple(User(*user_tuple) for user_tuple in db_execute(db, SQL_QUERY))


def db_get_user(db: DBCursor, user_id) -> User:
    SQL_QUERY = """
        SELECT
            user_id,
            email,
            user_type,
            name,
            pw_hash
        FROM user
        WHERE user_id = %s
    """
    user_tuples = db_execute(db, SQL_QUERY, (user_id,))
    if not user_tuples:
        raise ModelError(f"User with ID={user_id} does not exist.")
    return User(*user_tuples[0])


def db_get_user_by_email(db: DBCursor, email) -> User:
    SQL_QUERY = """
        SELECT user_id, email, user_type, name, pw_hash FROM user
        WHERE email = %s
    """
    user_tuples = db_execute(db, SQL_QUERY, (email,))
    if not user_tuples:
        raise ModelError("User with given email does not exist.")
    return User(*(user_tuples[0]))


def db_add_user(db: DBCursor, user_type, email, username, pw_hash: bytes) -> None:
    SQL_QUERY = """
        INSERT INTO user (user_type, email, name, pw_hash)
        VALUES (%s, %s, %s, %s)
    """
    db_execute(db, SQL_QUERY, (user_type, email, username, pw_hash))


def db_add_admin(db: DBCursor, email, username, pw_hash) -> None:
    SQL_QUERY = """
        INSERT INTO user (user_type, email, name, pw_hash)
        VALUES ('admin', %s, %s, %s)
    """
    db_execute(db, SQL_QUERY, (email, username, pw_hash))


def db_delete_user(db: DBCursor, user_id) -> None:
    SQL_QUERY = """
        DELETE FROM user
        WHERE user_id = %s
    """
    db_execute(db, SQL_QUERY, (user_id,))


def db_delete_user_by_email(db: DBCursor, user_email) -> None:
    SQL_QUERY = """
        DELETE FROM user
        WHERE email = %s
    """
    db_execute(db, SQL_QUERY, (user_email,))

