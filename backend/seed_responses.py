import asyncio
import sys
import os

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import get_database_pool, close_database_pool, execute_query

# Try to import chat_services, handle missing openai dependency
try:
    from services.chat_services import chat_with_gpt
    AI_AVAILABLE = True
except ImportError:
    print("⚠️  WARNING: 'openai' module not found. AI generation will be skipped.")
    print("   (This is likely due to the Windows Long Path issue. Move project to a shorter path to fix.)")
    AI_AVAILABLE = False
    def chat_with_gpt(user_input):
        return "AI not available"

# Test cases to seed
TEST_CASES = [
    {
        "breed_name_AKC_preRegis": "Labrador Retriever",
        "age_years_preReg": 0.5,
        "status_dietRelat_preReg": ["puppy", "sensitive stomach"],
        "description": "Puppy with sensitive stomach"
    },
    {
        "breed_name_AKC_preRegis": "Golden Retriever",
        "age_years_preReg": 12.0,
        "status_dietRelat_preReg": ["arthritis", "overweight"],
        "description": "Senior with arthritis and overweight"
    },
    {
        "breed_name_AKC_preRegis": "French Bulldog",
        "age_years_preReg": 3.0,
        "status_dietRelat_preReg": ["allergy"],
        "description": "Adult with allergy"
    },
    {
        "breed_name_AKC_preRegis": "Beagle",
        "age_years_preReg": 5.0,
        "status_dietRelat_preReg": ["none"],
        "description": "Healthy adult"
    },
    {
        "breed_name_AKC_preRegis": "German Shepherd",
        "age_years_preReg": 8.0,
        "status_dietRelat_preReg": ["health issues"],
        "description": "Senior with general health issues"
    }
]

async def seed_and_test():
    print("Initializing database connection...")
    try:
        await get_database_pool()
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        return

    print(f"\nSeeding {len(TEST_CASES)} responses and testing AI adaptation...\n")

    for case in TEST_CASES:
        breed = case["breed_name_AKC_preRegis"]
        age = case["age_years_preReg"]
        statuses = case["status_dietRelat_preReg"]
        status_str = ",".join(statuses)
        
        print(f"--- Case: {case['description']} ---")
        print(f"Input: {breed}, {age} years, Statuses: {statuses}")

        # Insert into DB
        try:
            await execute_query(
                """INSERT INTO questions_home_dog_4Q_v2 
                   (breed_name_AKC, age_years_preReg, status_dietRelat_preReg) 
                   VALUES ($1, $2, $3)""",
                breed, age, status_str
            )
            print("✅ Database Insert: Success")
        except Exception as e:
            print(f"❌ Database Insert Failed: {e}")

        # Test AI Generation
        # The AI prompt uses age and statuses.
        user_input = f"Age: {age}, Health Status: {status_str}"
        print(f"AI Prompt Input: '{user_input}'")
        
        try:
            # Note: chat_with_gpt is synchronous in the current implementation
            ai_response = chat_with_gpt(user_input)
            print("🤖 AI Response:")
            print(ai_response)
        except Exception as e:
            print(f"❌ AI Generation Failed: {e}")
        
        print("\n")

    await close_database_pool()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(seed_and_test())
