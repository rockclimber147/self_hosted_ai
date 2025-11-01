import psycopg
from db.connection import get_db_connection


def insert_user(email: str, hashed_password: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO 'user' (email, password)
                    VALUES (%s, %s)
                    RETURNING id, email, api_requests_left
                    """,
                    (email, hashed_password),
                )
                return cur.fetchone()
    except psycopg.errors.UniqueViolation:
        return None


def get_user_by_email(email: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, password, api_requests_left FROM "user" WHERE email = %s',
                (email,),
            )
            return cur.fetchone()


def get_user_by_id(user_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, email, api_requests_left FROM "user" WHERE id = %s',
                (user_id,),
            )
            return cur.fetchone()


def update_user_api_requests_left(user_id: int, amount: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE "user" SET api_requests_left = api_requests_left - %s WHERE id = %s',
                (amount, user_id),
            )
            conn.commit()