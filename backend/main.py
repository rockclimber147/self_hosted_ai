from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch

from fastapi.responses import JSONResponse
from fastapi import Request

from api import admin_router, user_router, ai_router
from ai.ai_class import SmolVLM2Wrapper

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.ai_model = SmolVLM2Wrapper(
        model_path="HuggingFaceTB/SmolVLM2-256M-Video-Instruct",
        device="cpu",
        dtype=torch.float32
    )
    print("AI model loaded!")
    yield




app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def all_exceptions_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": str(type(exc))}
    )

origins = ["http://127.0.0.1:5500", "http://localhost:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow all origins for testing
    allow_methods=["*"],  # allow POST, GET, etc.
    allow_headers=["*"],  # allow custom headers
    allow_credentials=True,  # allow cookies to be sent
)

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
