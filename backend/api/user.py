from fastapi import APIRouter, Depends, HTTPException, Response
from auth.security import hash_password, verify_password
from auth.jwt_handler import create_jwt
from auth.dependencies import get_current_user
from models.user import UserCreate, UserLogin, UserRead
from db.user import insert_user, get_user_by_email

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
def test():
    return {"message": "user route works"}


@router.get("/user-dashboard")
def user_dashboard(user_id: int = Depends(get_current_user)):
    return {"message": f"Welcome user {user_id}"}


@router.post("/create", response_model=UserRead)
def create_user(user: UserCreate):
    hashed_pw = hash_password(user.password)
    new_user = insert_user(user.email, hashed_pw)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return UserRead(
        id=new_user[0],
        email=new_user[1],
        api_requests_left=new_user[2],
    )

@router.post("/login")
def login_user(user: UserLogin, response: Response):
    row = get_user_by_email(user.email)
    if not row or not verify_password(user.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = row[0]
    token = create_jwt(user_id, role="user")
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Logged in successfully"}


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
