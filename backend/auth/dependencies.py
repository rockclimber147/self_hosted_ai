from fastapi import Request, HTTPException
from auth.jwt_handler import verify_jwt


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_jwt(token)
    if payload.get("role") != "user":
        raise HTTPException(status_code=403, detail="Forbidden: users only")
    return payload["sub"]  # user_id


def get_current_admin(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_jwt(token)
    print(payload)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: admins only")
    return payload["sub"]  # admin_id
