from fastapi import FastAPI

from api import admin_router, user_router, ai_router

app = FastAPI()
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}