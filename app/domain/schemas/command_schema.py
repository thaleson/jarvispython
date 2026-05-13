from pydantic import BaseModel


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    success: bool
    action: str
    message: str
