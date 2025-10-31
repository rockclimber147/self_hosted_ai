from fastapi import FastAPI, Request, UploadFile, File, APIRouter
from pathlib import Path


router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.get("/")
def test():
    return {"message": "ai"}


@router.post("/summarize/")
async def summarize_video(request: Request, file: UploadFile = File(...)):
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
    print(summary)
    return {"summary": summary}