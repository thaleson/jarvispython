from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/info")
async def system_info():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ollama_model": settings.OLLAMA_MODEL,
        "whisper_model": settings.WHISPER_MODEL,
        "status": "online",
    }
