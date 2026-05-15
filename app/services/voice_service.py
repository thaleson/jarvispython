from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.infrastructure.speech.microphone_recorder import MicrophoneRecorder
from app.infrastructure.speech.transcriber import AudioTranscriber
from app.services.command_service import CommandService


class VoiceService:
    @staticmethod
    def record_and_execute(
        duration: int = 5,
    ) -> dict:
        audio_path = MicrophoneRecorder.record(
            duration=duration,
        )

        return VoiceService.transcribe_and_execute(
            audio_path=audio_path,
        )

    @staticmethod
    async def upload_and_execute(
        audio_file: UploadFile,
    ) -> dict:
        Path("temp_audio").mkdir(
            exist_ok=True,
        )

        file_name = audio_file.filename or "audio.wav"

        file_extension = Path(file_name).suffix or ".wav"

        audio_path = f"temp_audio/{uuid4()}{file_extension}"

        content = await audio_file.read()

        with open(audio_path, "wb") as file:
            file.write(content)

        return VoiceService.transcribe_and_execute(
            audio_path=audio_path,
        )

    @staticmethod
    def transcribe_and_execute(
        audio_path: str,
    ) -> dict:
        transcriber = AudioTranscriber()

        text = transcriber.transcribe(
            audio_path,
        )

        result = CommandService.process_command(
            text,
        )

        return {
            "success": result.get("success", False),
            "transcription": text,
            "action": result.get("action"),
            "message": result.get("message"),
        }
