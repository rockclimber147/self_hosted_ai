from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_methods=["*"],  # allow POST, GET, etc.
    allow_headers=["*"],  # allow custom headers
)

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}