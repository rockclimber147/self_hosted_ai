from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List

from auth.jwt_handler import create_jwt
from auth.security import hash_password, verify_password
from auth.dependencies import get_current_admin
from db.admin import get_admin_by_email, get_admin_by_id, insert_admin
from db.user import get_all_users
from db.stats import get_endpoint_stats
from models.admin import AdminCreate, AdminLogin, AdminRead, AdminAuth
from models.user import UserRead
from models.endpoint_access import EndpointStatRead
from db.user import get_user_by_id, update_user_requests_remaining, delete_user_by_id

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
def test():
    return {"message": "admin route works"}


@router.get("/get_admin_info")
def get_admin_info(admin_id: int = Depends(get_current_admin)):
    admin: AdminRead = get_admin_by_id(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@router.post(
    "/create",
    response_model=AdminRead,
)
def create_admin(admin: AdminCreate, response: Response):
    hashed_pw = hash_password(admin.password)
    new_admin = insert_admin(admin.email, hashed_pw)

    if not new_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin_id = new_admin.id
    token = create_jwt(admin_id, role="admin")
    response.set_cookie(
        key="access_token", value=token, httponly=True, secure=True, samesite="None"
    )

    return AdminRead(id=new_admin.id, email=new_admin.email)


@router.post("/login")
def login_admin(admin: AdminLogin, response: Response):
    row = get_admin_by_email(admin.email)
    if not row or not verify_password(admin.password, row.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    admin_id = row.id
    token = create_jwt(admin_id, role="admin")
    response.set_cookie(
        key="access_token", value=token, httponly=True, secure=True, samesite="None"
    )
    return {"message": "Logged in successfully"}


@router.post("/logout")
def logout_admin(response: Response):
    response.delete_cookie(
        key="access_token", httponly=True, secure=True, samesite="None"
    )
    return {"message": "Logged out successfully"}


@router.get("/users", response_model=List[UserRead])
def get_all_users_endpoint(admin_id: int = Depends(get_current_admin)):
    """Get all users and their remaining API requests (admin only)"""
    users = get_all_users()
    return users


@router.get("/endpoint_access", response_model=List[EndpointStatRead])
def get_all_endpoint_data(admin_id: int = Depends(get_current_admin)):
    stats = get_endpoint_stats()
    return stats


@router.delete("/user/{user_id}", response_model=dict)
def delete_user(user_id: int, admin_id: int = Depends(get_current_admin)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = delete_user_by_id(user_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    return {"message": f"User {user_id} deleted successfully"}


@router.patch("/user/{user_id}/requests")
def update_user_requests_endpoint(
    user_id: int, requests_remaining: int, admin_id: int = Depends(get_current_admin)
):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = update_user_requests_remaining(user_id, requests_remaining)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")
    return updated_user
