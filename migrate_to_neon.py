import os
import sqlite3

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

NEON_DATABASE_URL = os.getenv("DATABASE_URL")

if not NEON_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Check your .env file."
    )


# =========================================================
# SQLITE SOURCE DATABASE
# =========================================================

SQLITE_PATH = os.path.join(
    os.path.dirname(__file__),
    "instance",
    "hope_journal.db"
)

if not os.path.exists(SQLITE_PATH):
    raise FileNotFoundError(
        f"SQLite database not found:\n{SQLITE_PATH}"
    )


# =========================================================
# CONNECT TO SQLITE
# =========================================================

print("Connecting to SQLite...")

sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_conn.row_factory = sqlite3.Row


# =========================================================
# CONNECT TO NEON POSTGRESQL
# =========================================================

print("Connecting to Neon PostgreSQL...")

neon_engine = create_engine(
    NEON_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require"
    }
)


# =========================================================
# TABLES
# =========================================================
#
# IMPORTANT:
# The order matters because some tables contain
# foreign keys pointing to other tables.
#
# users
#   ↓
# journal_entries
#   ↓
# ai_responses
#
# prayers and reflections also reference users
# and journal_entries.
# =========================================================

tables = [
    "users",
    "journal_entries",
    "ai_responses",
    "scriptures",
    "prayers",
    "reflections",
]


# =========================================================
# CHECK NEON DATABASE
# =========================================================

print("\nChecking Neon database...")

try:

    with neon_engine.connect() as conn:

        for table in tables:

            result = conn.execute(
                text(
                    f'SELECT COUNT(*) FROM "{table}"'
                )
            )

            count = result.scalar()

            print(
                f"  {table}: {count} records"
            )

except Exception:

    sqlite_conn.close()
    neon_engine.dispose()

    raise


# =========================================================
# SHOW SQLITE SOURCE COUNTS
# =========================================================

print("\nChecking SQLite source database...")

sqlite_counts = {}

for table in tables:

    count = sqlite_conn.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    ).fetchone()[0]

    sqlite_counts[table] = count

    print(
        f"  {table}: {count} records"
    )


# =========================================================
# CONFIRM MIGRATION
# =========================================================

print("\n" + "=" * 60)
print("MIGRATION SAFETY CHECK")
print("=" * 60)

print(
    "\nThe migration will copy data FROM:"
)

print(
    f"  {SQLITE_PATH}"
)

print(
    "\nTO:"
)

print(
    "  Neon PostgreSQL"
)

print(
    "\nYour SQLite database will NOT be deleted or modified."
)

print(
    "\nExisting records in Neon will NOT be overwritten."
)

print(
    "\nSQLite records available for migration:"
)

for table in tables:

    print(
        f"  {table}: {sqlite_counts[table]}"
    )

print(
    "\n" + "=" * 60
)

try:

    answer = input(
        "\nType MIGRATE to continue: "
    ).strip()

except EOFError:

    print(
        "\nNo confirmation received."
    )

    print(
        "Migration cancelled. No data was changed."
    )

    sqlite_conn.close()
    neon_engine.dispose()

    raise SystemExit


if answer != "MIGRATE":

    print(
        "\nMigration cancelled."
    )

    print(
        "No data was changed."
    )

    sqlite_conn.close()
    neon_engine.dispose()

    raise SystemExit


# =========================================================
# MIGRATION
# =========================================================

print("\nStarting migration...")

try:

    with neon_engine.begin() as neon_conn:

        for table in tables:

            print(
                f"\nMigrating table: {table}"
            )

            # -------------------------------------------------
            # GET SQLITE COLUMN NAMES
            # -------------------------------------------------

            columns_info = sqlite_conn.execute(
                f'PRAGMA table_info("{table}")'
            ).fetchall()

            columns = [
                row["name"]
                for row in columns_info
            ]

            if not columns:

                raise RuntimeError(
                    f"Could not find columns for table '{table}'."
                )


            # -------------------------------------------------
            # GET SQLITE RECORDS
            # -------------------------------------------------

            rows = sqlite_conn.execute(
                f'SELECT * FROM "{table}"'
            ).fetchall()

            print(
                f"  SQLite records found: {len(rows)}"
            )

            if not rows:

                print(
                    "  Nothing to migrate."
                )

                continue


            # -------------------------------------------------
            # BUILD INSERT STATEMENT
            # -------------------------------------------------

            column_names = ", ".join(
                f'"{column}"'
                for column in columns
            )

            parameter_names = ", ".join(
                f":{column}"
                for column in columns
            )

            insert_sql = text(
                f'''
                INSERT INTO "{table}"
                ({column_names})
                VALUES
                ({parameter_names})
                ON CONFLICT DO NOTHING
                '''
            )


            # -------------------------------------------------
            # INSERT RECORDS
            # -------------------------------------------------

            inserted = 0
            skipped = 0

            for row in rows:

                data = dict(row)

                result = neon_conn.execute(
                    insert_sql,
                    data
                )

                if result.rowcount == 1:

                    inserted += 1

                else:

                    skipped += 1


            print(
                f"  Inserted: {inserted}"
            )

            print(
                f"  Already existed/skipped: {skipped}"
            )


    # =====================================================
    # MIGRATION SUCCESS
    # =====================================================

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)


    # =====================================================
    # SQLITE FINAL COUNTS
    # =====================================================

    print("\nSQLite source counts:")

    for table in tables:

        count = sqlite_conn.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]

        print(
            f"  {table}: {count}"
        )


    # =====================================================
    # NEON FINAL COUNTS
    # =====================================================

    print("\nNeon destination counts:")

    with neon_engine.connect() as conn:

        for table in tables:

            count = conn.execute(
                text(
                    f'SELECT COUNT(*) FROM "{table}"'
                )
            ).scalar()

            print(
                f"  {table}: {count}"
            )


    # =====================================================
    # FINAL VERIFICATION
    # =====================================================

    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)

    migration_matches = True

    with neon_engine.connect() as conn:

        for table in tables:

            sqlite_count = sqlite_conn.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]

            neon_count = conn.execute(
                text(
                    f'SELECT COUNT(*) FROM "{table}"'
                )
            ).scalar()

            if sqlite_count == neon_count:

                print(
                    f"  {table}: MATCH "
                    f"({sqlite_count} records)"
                )

            else:

                migration_matches = False

                print(
                    f"  {table}: MISMATCH "
                    f"(SQLite={sqlite_count}, "
                    f"Neon={neon_count})"
                )


    # =====================================================
    # FINAL RESULT
    # =====================================================

    print("\n" + "=" * 60)

    if migration_matches:

        print(
            "SUCCESS: SQLite and Neon record counts match."
        )

        print(
            "Your data has been migrated successfully."
        )

        print(
            "Your original SQLite database remains untouched."
        )

    else:

        print(
            "WARNING: Some record counts do not match."
        )

        print(
            "Do NOT delete the SQLite database."
        )

        print(
            "We should investigate the mismatch before"
            " continuing."
        )

    print("=" * 60)


except Exception as error:

    print("\n" + "=" * 60)
    print("MIGRATION FAILED")
    print("=" * 60)

    print(
        f"\nError: {error}"
    )

    print(
        "\nNo changes were made to the SQLite database."
    )

    print(
        "Do NOT delete your SQLite database."
    )

    print(
        "\nWe need to inspect the error before trying again."
    )

    raise


finally:

    sqlite_conn.close()
    neon_engine.dispose()

