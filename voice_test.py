from app.infrastructure.speech.microphone_recorder import MicrophoneRecorder
from app.infrastructure.speech.transcriber import AudioTranscriber
from app.services.command_service import CommandService

print("🎤 Gravando...")

audio_path = MicrophoneRecorder.record(
    duration=5,
)

print("🧠 Transcrevendo...")

transcriber = AudioTranscriber()

text = transcriber.transcribe(
    audio_path,
)

print(f"Você disse: {text}")

print("⚡ Executando comando...")

result = CommandService.process_command(
    text,
)

print(result)

input("Pressione ENTER para encerrar...")
