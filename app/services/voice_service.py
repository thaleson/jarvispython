from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.infrastructure.speech.piper_tts_engine import PiperTTSEngine
from app.infrastructure.speech.transcriber import AudioTranscriber
from app.infrastructure.speech.vad_recorder import VADRecorder
from app.services.command_service import CommandService
from app.services.conversation_service import ConversationService
from app.services.intent_service import IntentService
from app.services.response_service import ResponseService


class VoiceService:
    @staticmethod
    def record_and_execute(
        duration: int = 5,
    ) -> dict:
        audio_path = VADRecorder.record()

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

        try:
            return VoiceService.transcribe_and_execute(
                audio_path=audio_path,
            )
        finally:
            Path(audio_path).unlink(
                missing_ok=True,
            )

    @staticmethod
    def transcribe_and_execute(
        audio_path: str,
    ) -> dict:
        transcriber = AudioTranscriber()

        text = transcriber.transcribe(
            audio_path,
        )

        intent = IntentService.detect_intent(
            text,
        )

        if intent.get("action") == "conversation":
            conversation_response = ConversationService.generate_response(
                intent.get("query", text),
            )

            tts = PiperTTSEngine()
            tts.speak(
                conversation_response,
            )

            return {
                "success": True,
                "transcription": text,
                "action": "conversation",
                "message": conversation_response,
            }

        result = CommandService.process_command(
            text,
        )

        message = result.get("message")

        spoken_response = ResponseService.generate_spoken_response(
            action=result.get("action"),
            message=message,
            query=result.get("query"),
        )

        if spoken_response:
            tts = PiperTTSEngine()
            tts.speak(
                spoken_response,
            )

        return {
            "success": result.get("success", False),
            "transcription": text,
            "action": result.get("action"),
            "message": message,
        }
