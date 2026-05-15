from fastapi import FastAPI

from app.api.routes.command_route import router as command_router
from app.api.routes.health_route import router as health_router
from app.api.routes.voice_route import router as voice_router

app = FastAPI(
    title="Jarvis AI",
    description="Local AI Assistant",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(command_router)
app.include_router(voice_router)
