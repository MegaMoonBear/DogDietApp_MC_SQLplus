import asyncio
import os
from dotenv import load_dotenv
import asyncpg

# Load environment from repo root and backend/.env as fallback
load_dotenv()
if not os.getenv('DATABASE_URL'):
    # Try backend/.env if root .env doesn't exist
    load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # Fail fast with a clear message if the DB URL is missing
    raise SystemExit('DATABASE_URL not found in environment')

async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Query: list columns and types for the breeds table
        print('Running column info query for breedsakc_ids_v3...')
        cols = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='breedsakc_ids_v3'
            ORDER BY ordinal_position;
        """)
        for r in cols:
            print(f"{r['column_name']:30} | {r['data_type']}")

        # Query: count rows to confirm seed/creation
        print('\nRunning row count for breedsakc_ids_v3...')
        count = await conn.fetchval('SELECT COUNT(*) FROM breedsakc_ids_v3;')
        print('Row count:', count)
        
        # --- questions table checks ---
        # Query: list columns for the questions table (columns are lowercased in Postgres)
        print('\nRunning column info query for questions_home_dog_4q_v2...')
        qcols = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='questions_home_dog_4q_v2'
            ORDER BY ordinal_position;
        """)
        for r in qcols:
            print(f"{r['column_name']:30} | {r['data_type']}")

        # Query: count rows in the questions table
        print('\nRunning row count for questions_home_dog_4q_v2...')
        qcount = await conn.fetchval('SELECT COUNT(*) FROM questions_home_dog_4q_v2;')
        print('Row count:', qcount)
    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())