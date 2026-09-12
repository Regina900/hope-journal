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
print()

with engine.connect() as conn:

    print("=" * 60)
    print("NEON DATABASE VERIFICATION")
    print("=" * 60)

    # 1. Verify record counts
    print("\nRecord counts:")

    for table in tables:
        result = conn.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )
        count = result.scalar()

        print(f"  {table}: {count}")

    # 2. Show users
    print("\nUsers:")

    result = conn.execute(
        text("""
            SELECT id, username, created_at
            FROM users
            ORDER BY id
        """)
    )

    for row in result:
        print(f"  ID {row.id}: {row.username} | created: {row.created_at}")

    # 3. Show journal entries
    print("\nJournal entries:")

    result = conn.execute(
        text("""
            SELECT id, user_id, mood, created_at
            FROM journal_entries
            ORDER BY id
        """)
    )

    for row in result:
        print(
            f"  ID {row.id}: "
            f"user_id={row.user_id}, "
            f"mood={row.mood}, "
            f"created={row.created_at}"
        )

    # 4. Show AI response relationships
    print("\nAI responses:")

    result = conn.execute(
        text("""
            SELECT id, journal_entry_id, emotional_state, scripture_reference
            FROM ai_responses
            ORDER BY id
        """)
    )

    for row in result:
        print(
            f"  ID {row.id}: "
            f"journal_entry_id={row.journal_entry_id}, "
            f"state={row.emotional_state}, "
            f"scripture={row.scripture_reference}"
        )

print()
print("=" * 60)
print("SUCCESS: Neon data verification completed.")
print("=" * 60)