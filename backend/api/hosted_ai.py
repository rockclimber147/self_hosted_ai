from fastapi import APIRouter

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.get("/")
def test():
    return {"message": "ai"}