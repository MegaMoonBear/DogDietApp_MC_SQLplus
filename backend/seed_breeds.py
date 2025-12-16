import asyncio
import os
from dotenv import load_dotenv
import asyncpg

# Load environment variables from .env (repo root) and fallback to backend/.env
load_dotenv()
if not os.getenv('DATABASE_URL'):
    load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise SystemExit('DATABASE_URL not found in environment')

# Sample breed rows to insert: (breed_name_AKC, dogapi_id)
# Provide these as tuples; they will be upserted into the table.
BREEDS = [
    ("Other, including other breeds, mixed breed, unsure, and others", "00000000-0000-0000-0000-000000000000"),
    ("American Staffordshire Terrier", "30a056b8-2bbe-4aa9-b874-c511eb2ca775"),
    ("Beagle", "d8621d92-6558-451c-8631-a32e767026a0"),
    ("Chihuahua", "092dae18-86f4-4b41-a3f8-f57fab2f6f2c"),
    ("French Bulldog", "1fa29da4-8cc9-4f82-9c4d-cd93ee6dd6be"),
    ("Golden Retriever", "fee91641-2a2e-4c4f-b557-cff67c5803bc"),
    ("Labrador Retriever", "9d7c4db8-b9cf-4ed3-af8e-86fc56fbf251"),
    ("Shih Tzu", "e4aa816d-fb22-4841-80c4-b9967c310447"),
    ("Staffordshire Bull Terrier", "791fa86c-ff6c-49d9-92ee-b33c755ca50e"),
    ("Yorkshire Terrier", "ce40589c-295a-4259-9e83-711854db8129"),
]

async def seed():
    # Connect to the database and run inserts inside an async context
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Use an upsert so repeated runs update dogapi_id if the breed already exists
        insert_sql = """
            INSERT INTO breedsAKC_IDs_v3 (breed_name_AKC, dogapi_id)
            VALUES ($1, $2)
            ON CONFLICT (breed_name_AKC) DO UPDATE SET dogapi_id = EXCLUDED.dogapi_id
        """

        # Execute insertion for each sample row
        for name, dogid in BREEDS:
            await conn.execute(insert_sql, name, dogid)
        print("Inserted/updated sample breeds.")

        # Verify the rows were inserted by fetching by dogapi_id values
        ids = [b[1] for b in BREEDS]
        rows = await conn.fetch(
            "SELECT breed_name_AKC, dogapi_id FROM breedsAKC_IDs_v3 WHERE dogapi_id = ANY($1::text[])",
            ids,
        )

        # Print results. asyncpg returns lowercase column names by default,
        # so handle both casings when accessing dict keys.
        print('\nRows inserted:')
        for r in rows:
            name = r.get('breed_name_AKC') or r.get('breed_name_akc')
            dogid = r.get('dogapi_id')
            print(f"  - {name} | {dogid}")

    finally:
        # Always close the connection
        await conn.close()

if __name__ == '__main__':
    # Entry point: run the async seed function
    asyncio.run(seed())
