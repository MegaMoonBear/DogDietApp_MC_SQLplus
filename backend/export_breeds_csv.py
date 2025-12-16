import os
import csv
import asyncio
from dotenv import load_dotenv
import asyncpg

# Load env vars
load_dotenv()
if not os.getenv('DATABASE_URL'):
    load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise SystemExit('DATABASE_URL not found in environment')

OUT_CSV = 'backend/breedsAKC_IDs_v3.csv'

async def export():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch('SELECT * FROM breedsAKC_IDs_v3 ORDER BY breed_name_AKC;')
        if not rows:
            print('No rows found in breedsAKC_IDs_v3; CSV will be empty with header.')

        # Use column names from first row if available, otherwise query information_schema
        if rows:
            columns = list(rows[0].keys())
        else:
            cols = await conn.fetch("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='breedsakc_ids_v3' ORDER BY ordinal_position;
            """)
            columns = [c['column_name'] for c in cols]

        # Write CSV
        with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for r in rows:
                writer.writerow([r.get(col) for col in columns])

        print(f'Wrote CSV: {OUT_CSV}')

        # Print preview (first 10 rows)
        print('\nPreview:')
        with open(OUT_CSV, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                print(line.strip())
                if i >= 10:
                    break

    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(export())
