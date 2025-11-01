from pydantic import BaseModel


class AdminCreate(BaseModel):
    email: str
    password: str


class AdminLogin(BaseModel):
    email: str
    password: str


class AdminRead(BaseModel):
    id: int
    email: str
