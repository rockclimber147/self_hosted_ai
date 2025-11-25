from fastapi import Request, UploadFile, File, APIRouter, HTTPException, Depends
from pathlib import Path
from auth.dependencies import get_current_user
from db.user import get_user_by_id, update_user_api_requests_left


router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.get("/")
def test():
    return {"message": "ai"}


@router.post("/summarize/")
async def summarize_video(request: Request, file: UploadFile = File(...), user_id: int = Depends(get_current_user)):

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    api_requests_left = user.api_requests_left  # api_requests_left is the third column
    warning = None
    if api_requests_left <= 0:
        warning = "You have exceeded your free API requests. You may still use the service, but future limits may apply."
    else:
        # Decrement the request count only if they have remaining quota
        update_user_api_requests_left(user_id, 1)

    
    # Access the model
    ai_model = request.app.state.ai_model

    # Save the uploaded file
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    video_path = uploads_dir / file.filename

    with open(video_path, "wb") as f:
        f.write(await file.read())
    print(video_path)

    # Run inference
    summary = ai_model.summarize_video(str(video_path))

    response = {"summary": summary}
    if warning:
        response["warning"] = warning
    return response
