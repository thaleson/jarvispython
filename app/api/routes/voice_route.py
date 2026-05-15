from fastapi import APIRouter, File, UploadFile

from app.services.voice_service import VoiceService

router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
)


@router.post("/record")
async def record_voice():
    return VoiceService.record_and_execute(
        duration=5,
    )


@router.post("/upload")
async def upload_voice(
    audio_file: UploadFile = File(...),
):
    return await VoiceService.upload_and_execute(
        audio_file=audio_file,
    )
