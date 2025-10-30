### User routes here
from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/")
def test():
    return {"message": "user"}

@router.post("/create")
def create_user():
    ...

@router.post("/login")
def login_user():
    ...