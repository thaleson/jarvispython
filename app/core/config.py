from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Jarvis AI"
    VERSION: str = "1.0.0"


settings = Settings()
