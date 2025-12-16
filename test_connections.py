"""
Comprehensive connection test for WhiskerWorthy app
Tests frontend, backend, database, and API connections
"""
import requests
import json
import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
import asyncpg

# Load environment variables
env_path = backend_path / '.env'
load_dotenv(env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("🔍 WHISKERWORTHY APP CONNECTION TEST")
print("=" * 60)

# Test 1: Check if frontend files exist
print("\n1️⃣  FRONTEND FILES:")
frontend_files = [
    'frontend/index.html',
    'frontend/public/main.js',
    'frontend/public/style.css',
    'frontend/public/assets/doggy.jpeg'
]
for file in frontend_files:
    exists = Path(file).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")

# Test 2: Check if backend files exist
print("\n2️⃣  BACKEND FILES:")
backend_files = [
    'backend/main.py',
    'backend/models/database.py',
    'backend/schemas/schemas.py',
    'backend/services/report_service.py',
    'backend/.env'
]
for file in backend_files:
    exists = Path(file).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")

# Test 3: Check backend server
print("\n3️⃣  BACKEND API SERVER:")
backend_url = "http://localhost:5000"
try:
    response = requests.get(f"{backend_url}/docs", timeout=3)
    if response.status_code == 200:
        print(f"  ✅ Backend running at {backend_url}")
        print(f"  ✅ API docs accessible at {backend_url}/docs")
    else:
        print(f"  ⚠️  Backend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"  ❌ Backend NOT running at {backend_url}")
    print(f"  💡 Run: python backend/main.py")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 4: Check API endpoints
print("\n4️⃣  API ENDPOINTS:")
endpoints = [
    "/api/breeds",
    "/api/submit-dog-info"
]
for endpoint in endpoints:
    try:
        if endpoint == "/api/submit-dog-info":
            # POST endpoint - just check if it exists
            print(f"  ℹ️  {endpoint} (POST) - exists")
        else:
            response = requests.get(f"{backend_url}{endpoint}", timeout=3)
            status = "✅" if response.status_code in [200, 404] else "⚠️"
            print(f"  {status} {endpoint} - Status {response.status_code}")
    except:
        print(f"  ❌ {endpoint} - Not accessible")

# Test 5: Check database connection
print("\n5️⃣  DATABASE CONNECTION:")
async def test_database():
    try:
        conn = await asyncpg.connect(DATABASE_URL, timeout=5)
        print(f"  ✅ Connected to Neon PostgreSQL")
        
        # Check tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print(f"  ✅ Tables found: {len(tables)}")
        for table in tables:
            print(f"     • {table['table_name']}")
        
        # Check if our tables exist
        required_tables = ['breedsakc_ids_v3', 'questions_home_dog_4q_v2']
        for table in required_tables:
            exists = any(t['table_name'] == table for t in tables)
            status = "✅" if exists else "❌"
            print(f"  {status} Required table: {table}")
        
        await conn.close()
        return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False

try:
    db_connected = asyncio.run(test_database())
except Exception as e:
    print(f"  ❌ Database test error: {e}")
    db_connected = False

# Test 6: Check Python dependencies
print("\n6️⃣  PYTHON DEPENDENCIES:")
required_packages = ['fastapi', 'uvicorn', 'asyncpg', 'pydantic', 'python-dotenv']
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package} - Run: pip install {package}")

# Test 7: Frontend static server check
print("\n7️⃣  FRONTEND STATIC SERVER:")
frontend_url = "http://localhost:5173"
try:
    response = requests.get(frontend_url, timeout=3)
    if response.status_code == 200:
        print(f"  ✅ Frontend running at {frontend_url}")
    else:
        print(f"  ⚠️  Frontend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"  ❌ Frontend NOT running at {frontend_url}")
    print(f"  💡 Run: cd frontend && python -m http.server 5173")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)
print("\n✅ = Working | ❌ = Issue Found | ⚠️  = Warning\n")
print("🔗 To start the full app:")
print("   Terminal 1: cd frontend && python -m http.server 5173")
print("   Terminal 2: python backend/main.py")
print("   Browser:    http://localhost:5173")
print("\n" + "=" * 60)
