#  beginner-friendly options inside or alongside VS Code:

# View table contents (PostgreSQL)  AND  Add records into breedsAKC_IDs_v3*
# pgAdmin 4 (Elephant logo) Connect to Neon database using connection details from your Neon dashboard.
        # INSERT INTO breedsAKC_IDs_v3 (breed_name_AKC, dogapi_id)
        # VALUES ('Beagle', 'ID_35alphanumeric__ID_35alphanumeric');
# The FastAPI POST /api/breed currently expects more fields; for minimal inserts use direct SQL (pgAdmin/psql) as above, or extend the API to make those fields optional.


# Temporary script to check if tables exist in Neon database
import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def check_tables():
    """Check if tables exist in the database"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Check if tables exist
        result = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print("\n📋 Tables in database:")
        if result:
            for row in result:
                print(f"  ✅ {row['table_name']}")
        else:
            print("  ❌ No tables found!")
        
        # Check specifically for our tables
        our_tables = ['breedsakc_ids_v3', 'questions_home_dog_4q_v2']
        print("\n🔍 Checking for required tables:")
        for table in our_tables:
            exists = await conn.fetchval(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            status = "✅ EXISTS" if exists else "❌ MISSING"
            print(f"  {table}: {status}")
            
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_tables())
