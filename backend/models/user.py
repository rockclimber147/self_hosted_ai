from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Public info model
class UserRead(BaseModel):
    id: int
    email: str
    api_requests_left: int

# Internal auth model (includes password)
class UserAuth(BaseModel):
    id: int
    email: str
    password: str
    api_requests_left: int