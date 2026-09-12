from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require"
    }
)

tables = [
    "users",
    "journal_entries",
    "ai_responses",
    "scriptures",
    "prayers",
    "reflections",
]

print("Connecting to Neon PostgreSQL...")

with engine.begin() as conn:
    for table in tables:
        print(f"Resetting sequence for {table}...")

        conn.execute(
            text(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('{table}', 'id'),
                    COALESCE((SELECT MAX(id) FROM {table}), 1)
                )
                """
            )
        )

print()
print("=" * 60)
print("SUCCESS: PostgreSQL ID sequences have been reset.")
print("=" * 60)