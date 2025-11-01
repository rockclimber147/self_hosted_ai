from fastapi import APIRouter, Depends, HTTPException, Response

from auth.jwt_handler import create_jwt
from auth.security import hash_password, verify_password
from auth.dependencies import get_current_admin
from db.admin import get_admin_by_email, insert_admin
from models.admin import AdminCreate, AdminLogin, AdminRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
def test():
    return {"message": "admin route works"}


@router.get("/admin-dashboard")
def admin_dashboard(admin_id: int = Depends(get_current_admin)):
    return {"message": f"Welcome admin {admin_id}"}


@router.post("/create", response_model=AdminRead)
def create_admin(admin: AdminCreate):
    hashed_pw = hash_password(admin.password)
    new_admin = insert_admin(admin.email, hashed_pw)

    if not new_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")

    return AdminRead(
        id=new_admin[0],
        email=new_admin[1],
    )


@router.post("/login")
def login_admin(admin: AdminLogin, response: Response):
    row = get_admin_by_email(admin.email)
    if not row or not verify_password(admin.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    admin_id = row[0]
    token = create_jwt(admin_id, role="admin")
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Logged in successfully"}


@router.post("/logout")
def logout_admin(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
