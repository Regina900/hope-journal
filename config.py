import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Flask security
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-this"
    )

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hope_journal.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL / Neon connection settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # AI configuration
    AI_MODE = os.getenv("AI_MODE", "demo")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Application limits
    MAX_JOURNAL_LENGTH = 5000
    MAX_USERNAME_LENGTH = 50
    MAX_PASSWORD_LENGTH = 128