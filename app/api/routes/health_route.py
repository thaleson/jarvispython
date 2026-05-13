from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health_check():
    return {
        "status": "online",
        "service": "jarvis-ai",
        "version": "1.0.0",
        "uptime": "24 hours",
        "message": "Jarvis AI is running smoothly oray!",
    }
