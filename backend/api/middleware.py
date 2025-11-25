from fastapi import Request
from db.stats import increment_endpoint_count

def user_route_stats_dependency(request: Request):
    endpoint = request.scope["path"]
    method = request.method
    increment_endpoint_count(endpoint, method)


async def count_requests_middleware(request: Request, call_next):
    # Extract path and method
    endpoint = request.url.path
    method = request.method

    if method == "DELETE":
        endpoint = "/admin/user"
    if method == "PATCH":
        endpoint = "/admin/user"

    # Update database counter
    increment_endpoint_count(endpoint, method)

    # Continue processing the request
    response = await call_next(request)
    return response