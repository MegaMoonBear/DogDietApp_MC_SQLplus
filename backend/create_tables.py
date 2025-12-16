# Script to create tables in Neon database
import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def create_tables():
    """Create the required tables in the database"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("🔨 Creating tables...")
        
        # Create breeds table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS breedsAKC_IDs_v3 (
              breed_name_AKC TEXT PRIMARY KEY,
              breed_group_AKC TEXT,
              breed_life_expect_yrs DECIMAL(3,1),
              listed_DogDiet_MVP CHAR(1),
              food_recomm_product TEXT,
              dogapi_id TEXT
            );
        """)
        print("  ✅ Created table: breedsAKC_IDs_v3")
        
        # Create questions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS questions_home_dog_4Q_v2 (
              id_dog_preRegis SERIAL PRIMARY KEY,
              breed_name_AKC TEXT,
              age_years_preReg DECIMAL(3,1),
              status_dietRelat_preReg TEXT,
              modified_preReg TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("  ✅ Created table: questions_home_dog_4Q_v2")
        
        # Verify tables were created
        result = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print("\n✅ Tables now in database:")
        for row in result:
            print(f"  • {row['table_name']}")
            
        print("\n🎉 Database setup complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_tables())
