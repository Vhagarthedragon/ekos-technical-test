"""Run all SQL migration files in order."""
import asyncio
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def run_migrations():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL not set")

    print("Connecting to database...")
    conn = await asyncpg.connect(url)

    for sql_file in sorted(Path(__file__).parent.glob("*.sql")):
        print(f"  Running {sql_file.name}...")
        await conn.execute(sql_file.read_text(encoding="utf-8"))
        print(f"  Done.")

    await conn.close()
    print("Migrations complete.")


if __name__ == "__main__":
    asyncio.run(run_migrations())
