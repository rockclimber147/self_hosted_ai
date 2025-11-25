from pydantic import BaseModel

# Input models
class AdminCreate(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str

# Output model for public info
class AdminRead(BaseModel):
    id: int
    email: str

# Internal model for authentication (includes password)
class AdminAuth(BaseModel):
    id: int
    email: str
    password: str