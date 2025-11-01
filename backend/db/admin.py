import psycopg
from db.connection import get_db_connection


def insert_admin(email: str, hashed_password: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO admin (email, password)
                    VALUES (%s, %s)
                    RETURNING id, email
                    """,
                    (email, hashed_password),
                ) 
                return cur.fetchone()
    except psycopg.errors.UniqueViolation:
        return None


def get_admin_by_email(email: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, password FROM admin WHERE email = %s",
                (email,),
            )
            return cur.fetchone()

def get_admin_by_id(admin_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, email FROM admin WHERE id = %s",
                (admin_id,),
            )
            return cur.fetchone()