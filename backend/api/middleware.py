from fastapi import Request
from db.stats import increment_endpoint_count

def user_route_stats_dependency(request: Request):
    endpoint = request.scope["path"]
    method = request.method
    increment_endpoint_count(endpoint, method)