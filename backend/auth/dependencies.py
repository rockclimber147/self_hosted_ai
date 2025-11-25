from fastapi import Request, HTTPException
from auth.jwt_handler import verify_jwt
from db.user import increment_user_total_api_calls

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    result = verify_jwt(token)
    if not result.get("success"):
        print(f"ERROR: Token verification failed: {result.get('error')}")
        raise HTTPException(status_code=401, detail=result.get("error", "Invalid token"))
    payload = result["payload"]
    if payload.get("role") != "user":
        raise HTTPException(status_code=403, detail="Forbidden: users only")
    user_id = int(payload["sub"])
    increment_user_total_api_calls(user_id)
    return int(payload["sub"])  # Convert back to int since we stored it as string


def get_current_admin(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = verify_jwt(token)
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error", "Invalid token"))
    payload = result["payload"]
    print(payload)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: admins only")
    return int(payload["sub"])  # Convert back to int since we stored it as string
