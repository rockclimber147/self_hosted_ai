import psycopg
from psycopg.rows import dict_row
from db.connection import get_db_connection
from models.user import UserRead, UserAuth


def insert_user(email: str, hashed_password: str) -> UserRead | None:
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO "user" (email, password)
                    VALUES (%s, %s)
                    RETURNING id, email, api_requests_left, total_api_calls, last_jwt
                    """,
                    (email, hashed_password),
                )
                row = cur.fetchone()
                if row:
                    return UserRead(**row)
                return None
    except psycopg.errors.UniqueViolation:
        return None


def get_user_by_email(email: str) -> UserAuth | None:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                'SELECT id, email, password, api_requests_left FROM "user" WHERE email = %s',
                (email,),
            )
            row = cur.fetchone()
            if row:
                return UserAuth(**row)
            return None


def get_user_by_id(user_id: int) -> UserRead | None:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                'SELECT * FROM "user" WHERE id = %s',
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                return UserRead(**row)
            return None


def update_user_api_requests_left(user_id: int, amount: int) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE "user" SET api_requests_left = api_requests_left - %s WHERE id = %s',
                (amount, user_id),
            )
            conn.commit()


def get_all_users() -> list[UserRead]:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "user" ORDER BY id')
            rows = cur.fetchall()
            return [UserRead(**row) for row in rows]


def increment_user_total_api_calls(user_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE "user"
                SET total_api_calls = total_api_calls + 1
                WHERE id = %s
                """,
                (user_id,),
            )
            conn.commit()


def set_user_last_jwt(user_id: int, last_jwt: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE "user"
                SET last_jwt = %s
                WHERE id = %s
                """,
                (last_jwt, user_id),
            )
            conn.commit()


def delete_user_by_id(user_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM "user"
                WHERE id = %s
                """,
                (user_id,),
            )
            affected = cur.rowcount
        conn.commit()
    return affected > 0


def update_user_requests_remaining(user_id: int, requests_remaining: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE "user"
                SET api_requests_left = %s
                WHERE id = %s
                RETURNING id, email, api_requests_left;
                """,
                (requests_remaining, user_id),
            )
            row = cur.fetchone()
            conn.commit()

            if row is None:
                return None
            updated_user = {
                "id": row["id"],
                "username": row["email"],
                "api_requests_left": row["api_requests_left"],
            }

            return updated_user
