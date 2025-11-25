from db.connection import get_db_connection
from models.endpoint_access import EndpointStatRead
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

def get_endpoint_stats() -> list[EndpointStatRead]:
    """Return all endpoint access stats as Pydantic models."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, endpoint, requests, method FROM endpoint_access ORDER BY endpoint DESC")
            rows = cur.fetchall()
            return [EndpointStatRead(**row) for row in rows]
