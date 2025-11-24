from pydantic import BaseModel

class EndpointStatRead(BaseModel):
    id: int
    endpoint: str
    requests: int
    method: str