import psycopg
from psycopg.rows import dict_row
from db.connection import get_db_connection
from models.admin import AdminRead, AdminAuth

def insert_admin(email: str, hashed_password: str) -> AdminAuth | None:
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO admin (email, password)
                    VALUES (%s, %s)
                    RETURNING id, email
                    """,
                    (email, hashed_password),
                )
                row = cur.fetchone()
                if row:
                    return AdminAuth(**row)
                return None
    except psycopg.errors.UniqueViolation:
        return None

def get_admin_by_email(email: str) -> AdminAuth | None:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, email, password FROM admin WHERE email = %s",
                (email,),
            )
            row = cur.fetchone()
            if row:
                return AdminAuth(**row)
            return None

def get_admin_by_id(admin_id: int) -> AdminRead | None:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, email FROM admin WHERE id = %s",
                (admin_id,),
            )
            row = cur.fetchone()
            if row:
                return AdminRead(**row)
            return None
