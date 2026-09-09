import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hope_journal.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI configuration
    AI_MODE = os.getenv("AI_MODE", "demo")
    AI_API_KEY = os.getenv("AI_API_KEY", "")

    # Application configuration
    MAX_JOURNAL_LENGTH = 5000
    MAX_USERNAME_LENGTH = 50
    MAX_PASSWORD_LENGTH = 128