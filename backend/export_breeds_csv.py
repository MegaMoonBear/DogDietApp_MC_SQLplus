import os
import csv
import asyncio
from dotenv import load_dotenv
import asyncpg

# Load environment variables; prefer repo root .env, fallback to backend/.env
load_dotenv()
if not os.getenv('DATABASE_URL'):
    load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # Critical: the script will not run without a valid DATABASE_URL
    raise SystemExit('DATABASE_URL not found in environment')

# Output CSV path (relative to repo root). Change if you want a different location.
OUT_CSV = 'backend/breedsAKC_IDs_v3.csv'

async def export():
    # Connect to Postgres using asyncpg
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Critical query: selects all columns from the live breeds table
        rows = await conn.fetch('SELECT * FROM breedsAKC_IDs_v3 ORDER BY breed_name_AKC;')
        if not rows:
            print('No rows found in breedsAKC_IDs_v3; CSV will be empty with header.')

        # Determine columns: prefer keys from the first returned row
        if rows:
            columns = list(rows[0].keys())  # asyncpg returns column names as dict keys
        else:
            # Fallback: query information_schema for column names (table_name is lowercase in Postgres)
            cols = await conn.fetch("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='breedsakc_ids_v3' ORDER BY ordinal_position;
            """)
            columns = [c['column_name'] for c in cols]

        # Write CSV header + rows
        with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for r in rows:
                # Use dict.get to avoid KeyError if casing differs
                writer.writerow([r.get(col) for col in columns])

        print(f'Wrote CSV: {OUT_CSV}')

        # Preview: print first ~10 lines to confirm contents
        print('\nPreview:')
        with open(OUT_CSV, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                print(line.strip())
                if i >= 10:
                    break

    finally:
        # Always close the DB connection
        await conn.close()

if __name__ == '__main__':
    # Run exporter when invoked directly
    asyncio.run(export())
