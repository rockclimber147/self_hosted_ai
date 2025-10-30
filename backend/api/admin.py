from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.post("/login")
def login_admin():
    ...

@router.get("/")
def test():
    return {"message": "admin"}