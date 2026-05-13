from fastapi import APIRouter

from app.domain.schemas.command_schema import CommandRequest, CommandResponse
from app.services.command_service import CommandService

router = APIRouter(
    prefix="/command",
    tags=["Command"],
)


@router.post(
    "/",
    response_model=CommandResponse,
)
async def process_command(
    payload: CommandRequest,
):

    action = CommandService.process_command(payload.command)

    return CommandResponse(
        success=True,
        action=action,
    )
