from pydantic import BaseModel


class VoiceResponse(BaseModel):
    success: bool
    transcription: str
    action: str | None
    message: str | None
