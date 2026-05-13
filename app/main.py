from fastapi import FastAPI

from app.api.routes.health_route import router as health_router

app = FastAPI(
    title="Jarvis AI",
    description="Local AI Assistant",
    version="1.0.0",
)

app.include_router(health_router)
