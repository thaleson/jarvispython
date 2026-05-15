from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Jarvis AI"

    APP_VERSION: str = "1.0.0"

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.2:1b"

    WHISPER_MODEL: str = "small"

    WHISPER_DEVICE: str = "cpu"

    WHISPER_COMPUTE_TYPE: str = "int8"

    VOICE_RECORD_DURATION: int = 5

    TEMP_AUDIO_DIR: str = "temp_audio"

    class Config:
        env_file = ".env"


settings = Settings()
