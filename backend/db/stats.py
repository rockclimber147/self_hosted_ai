from db.connection import get_db_connection
import psycopg

def increment_endpoint_count(endpoint: str, method: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO endpoint_access (endpoint, method, requests)
                VALUES (%s, %s, 1)
                ON CONFLICT (endpoint, method)
                DO UPDATE SET requests = endpoint_access.requests + 1
                """,
                (endpoint, method),
            )
            conn.commit()

def get_endpoint_stats(endpoint: str, method: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM endpoint_access
                """,
                (endpoint, method),
            )
            cur.fetchall()
