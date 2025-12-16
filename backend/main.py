# backend/main.py - FastAPI endpoint to receive form data and trigger report selection

# Routes (CRUD operations) for backend (API endpoints, Breed table, questionnaire submissions)
    # GET routes for retrieving breed data
    # POST routes for creating new records
    # PATCH route for partial updates (used by your admin form)
    # PUT route for full replacements


from fastapi import FastAPI, HTTPException, Path, Query  # Import FastAPI framework and utilities
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to allow frontend to call backend from different origin
from typing import List, Optional, Dict, Any  # Import type hints for better code clarity
import uvicorn  # Import uvicorn ASGI server to run FastAPI

# Import business logic from services folder
from services.report_service import choose_report  # Import the report selection function

# Import Pydantic schemas from schemas folder
from schemas.schemas import (
    DogQuestionnaireInput,  # User questionnaire input model
    BreedCreateInput,  # Create new breed input model
    BreedUpdateInput,  # Partial breed update input model
    BreedFullUpdateInput,  # Full breed replacement input model
    QuestionnaireResponse,  # Questionnaire response model
    StandardResponse  # Generic response model
)

# Import database connection functions from models folder
from models.database import (
    get_database_pool,  # Initialize connection pool
    close_database_pool,  # Close connection pool on shutdown
    execute_query,  # Execute INSERT/UPDATE queries
    fetch_one,  # Fetch single row
    fetch_all  # Fetch multiple rows
)

# Initialize FastAPI application
app = FastAPI(
    title="Dog Diet API",  # API title shown in automatic documentation
    description="API for dog diet recommendations and breed management",  # Description for docs
    version="1.0.0"  # Version number
)

# Configure CORS - allows frontend on different port/domain to access this API
app.add_middleware(
    CORSMiddleware,  # CORS middleware class
    allow_origins=["*"],  # List of allowed origins; "*" means all origins (restrict in production)
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PATCH, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ==================== Application Lifecycle Events ====================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the FastAPI application starts.
    Initializes the database connection pool.
    """
    await get_database_pool()  # Create database connection pool
    print("✅ Database connection pool initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the FastAPI application shuts down.
    Closes the database connection pool gracefully.
    """
    await close_database_pool()  # Close all database connections
    print("✅ Database connection pool closed")


# ==================== GET ROUTES - Retrieve Data ====================
# Note: Pydantic models have been moved to schemas/schemas.py for better organization

@app.get("/api/breeds")  # @app.get decorator maps URL path to function; automatically handles GET method
async def get_all_breeds():  # async allows for asynchronous operations (better performance)
    """
    GET endpoint to retrieve all breeds from database.
    Returns list of all breeds in breedsAKC_IDs_v3 table.
    """
    try:
        # Fetch all breeds from database
        breeds = await fetch_all("SELECT * FROM breedsAKC_IDs_v3 ORDER BY breed_name_AKC")
        
        return {  # FastAPI automatically converts dict to JSON response
            'success': True,
            'message': 'Retrieved all breeds',
            'breeds': breeds  # List of breed dictionaries from database
        }  # FastAPI automatically sets status code 200 for successful responses
        
    except Exception as e:  # Catch-all exception handler for any errors during execution
        raise HTTPException(status_code=500, detail=str(e))  # HTTPException returns error response; 500 = Internal Server Error


@app.get("/api/breed/{search_field}/{search_value}")  # {variable} in route captures URL segments as function parameters
async def get_breed(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),  # Path() provides validation and documentation
    search_value: str = Path(..., description="The breed name or ID to search for")
):
    """
    GET endpoint to retrieve a specific breed by breed_name_AKC or dogapi_id.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    # Validate search field - ensure only allowed field names to prevent SQL injection
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(  # HTTPException replaces return with error status
            status_code=400,  # 400 = Bad Request (client error)
            detail='Invalid search field. Use breed_name_AKC or dogapi_id'
        )
    
    try:
        # Fetch specific breed from database using parameterized query
        # Use $1 placeholder to prevent SQL injection (asyncpg uses $1, $2, etc.)
        query = f"SELECT * FROM breedsAKC_IDs_v3 WHERE {search_field} = $1"
        breed = await fetch_one(query, search_value)
        
        # Check if breed was found
        if not breed:
            raise HTTPException(
                status_code=404,  # 404 = Not Found
                detail=f'Breed not found with {search_field} = {search_value}'
            )
        
        return {
            'success': True,
            'message': f'Retrieved breed by {search_field}',  # f-string allows embedding variables directly in string
            'breed': breed  # Dictionary containing breed data from database
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== POST ROUTES - Create New Data ====================

# Preset questions tailored by simple inputs (stub; swap when real logic ready)
@app.get("/api/questions/preset")
async def get_preset_questions(
    breed_name_AKC: str = Query("", description="Breed name to tailor questions"),
    age_years_preReg: float | None = Query(None, description="Dog age in years"),
    status_dietRelat_preReg: List[str] | None = Query(None, description="Health status list")
):
    """Return up to three preset vet questions using provided context."""
    status_list = status_dietRelat_preReg or []

    questions = [
        f"Are there breed-specific nutrition concerns for {breed_name_AKC or 'my dog'}?",
        "Is the current body condition and weight on track for this age?",
        "Do any current conditions or meds change what diet you recommend?",
    ]

    if status_list:
        questions.append(f"How should diet change given these factors: {', '.join(status_list)}?")
    if age_years_preReg is not None:
        questions.append(f"Is this diet appropriate for a dog around {age_years_preReg} years old?")

    return {"success": True, "questions": questions[:3]}


# AI-generated questions (stubbed; replace with LLM later)
@app.post("/api/questions/ai")
async def generate_ai_questions(data: DogQuestionnaireInput):
    """Return three placeholder AI-style vet questions based on user input."""
    breed = data.breed_name_AKC or "the dog"
    statuses = ", ".join(data.status_dietRelat_preReg) if data.status_dietRelat_preReg else "none"

    ai_questions = [
        f"For {breed}, what diet best fits age {data.age_years_preReg} and statuses ({statuses})?",
        "Which lab checks should we monitor to confirm the diet is working?",
        "What signs would indicate we should adjust protein, fat, or calories?",
    ]

    # TODO: replace stub with real LLM integration
    return {"success": True, "questions": ai_questions}

@app.post("/api/submit-dog-info")  # @app.post decorator handles POST requests
async def submit_dog_info(data: DogQuestionnaireInput):  # Pydantic model automatically validates incoming JSON
    """
    POST endpoint - Receives dog questionnaire data from frontend form,
    calls the report selection logic, and returns the appropriate report.
    """
    try:
        # Extract validated data from Pydantic model (already parsed and validated)
        breed_name = data.breed_name_AKC  # Direct attribute access (no .get() needed with Pydantic)
        age_years = data.age_years_preReg
        status_list = data.status_dietRelat_preReg
        
        # Call the report selection function from services/report_service.py
        # Pass the status list and breed name to determine which report to use
        report_message = choose_report(status_list, breed_name)

        # Insert questionnaire data into database
        # Convert status_list array to comma-separated string for storage
        status_string = ','.join(status_list)  # Join list items with commas
        
        await execute_query(
            """INSERT INTO questions_home_dog_4Q_v2 
               (breed_name_AKC, age_years_preReg, status_dietRelat_preReg) 
               VALUES ($1, $2, $3)""",
            breed_name,  # $1 parameter
            age_years,   # $2 parameter
            status_string  # $3 parameter
        )
        
        # Return success response with the selected report message
        return {
            'success': True,
            'message': 'Dog information submitted successfully!',
            'report': report_message,  # The report selection result
            'breed': breed_name,
            'age': age_years,
            'statuses': status_list
        }  # FastAPI automatically returns with status code 200
        
    except Exception as e:
        # Catch any errors and return error response
        raise HTTPException(status_code=500, detail=str(e))  # 500 = Internal Server Error


@app.post("/api/breed", status_code=201)  # status_code=201 sets successful response code (Created)
async def create_breed(data: BreedCreateInput):  # Pydantic validates required breed_name_AKC automatically
    """
    POST endpoint to create a new breed record in breedsAKC_IDs_v3 table.
    Requires all necessary breed information in request body.
    """
    try:
        # Insert new breed into database with all provided fields
        await execute_query(
            """INSERT INTO breedsAKC_IDs_v3 
               (breed_name_AKC, breed_group_AKC, breed_life_expect_yrs, 
                listed_DogDiet_MVP, food_recomm_product, dogapi_id) 
               VALUES ($1, $2, $3, $4, $5, $6)""",
            data.breed_name_AKC,
            data.breed_group_AKC,
            data.breed_life_expect_yrs,
            data.listed_DogDiet_MVP,
            data.food_recomm_product,
            data.dogapi_id
        )
        
        return {
            'success': True,
            'message': 'Breed created successfully',
            'breed': data.breed_name_AKC
        }  # Returns with status_code=201 as specified in decorator
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== PATCH ROUTES - Partial Update ====================

@app.patch("/api/breed/{search_field}/{search_value}")  # @app.patch decorator handles PATCH requests
async def update_breed_partial(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to update"),
    data: BreedUpdateInput = None  # Pydantic model with all optional fields for partial updates
):
    """
    PATCH endpoint for partial updates to breed information.
    Only updates fields that are provided in request body.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    # Validate search field
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(
            status_code=400,
            detail='Invalid search field. Use breed_name_AKC or dogapi_id'
        )
    
    # Convert Pydantic model to dict and exclude None values (only get fields that were provided)
    update_data = data.dict(exclude_unset=True)  # exclude_unset=True only includes fields explicitly set by user
    
    # Check if there's data to update
    if not update_data:
        raise HTTPException(status_code=400, detail='No update data provided')
    
    try:
        # Build dynamic UPDATE query for only the fields provided
        # Create SET clause with parameterized queries
        set_clauses = [f"{key} = ${i+1}" for i, key in enumerate(update_data.keys())]
        set_string = ", ".join(set_clauses)  # Join with commas: "field1 = $1, field2 = $2"
        
        # Build full UPDATE query with WHERE clause
        query = f"UPDATE breedsAKC_IDs_v3 SET {set_string} WHERE {search_field} = ${len(update_data) + 1}"
        
        # Execute query with values from update_data dict, plus search_value at end
        await execute_query(query, *update_data.values(), search_value)
        
        # Build list of fields being updated (for response message)
        updated_fields = list(update_data.keys())  # .keys() returns dictionary keys; list() converts to array
        
        return {
            'success': True,
            'message': f'Breed updated successfully via {search_field}',
            'updated_fields': updated_fields,  # Shows which fields were modified
            'search_value': search_value  # Echo back the identifier used for confirmation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== PUT ROUTES - Full Update/Replace ====================

@app.put("/api/breed/{search_field}/{search_value}")  # @app.put decorator handles PUT requests
async def update_breed_full(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to update"),
    data: BreedFullUpdateInput = None  # Pydantic model with required fields for full replacement
):
    """
    PUT endpoint for full replacement of breed information.
    Requires all fields to be provided - replaces entire record.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    # Validate search field
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(
            status_code=400,
            detail='Invalid search field. Use breed_name_AKC or dogapi_id'
        )
    
    try:
        # Replace all breed fields in database with new data
        await execute_query(
            f"""UPDATE breedsAKC_IDs_v3 SET 
               breed_name_AKC = $1, breed_group_AKC = $2, breed_size_categ_AKC = $3,
               breed_life_expect_yrs = $4, food_recomm_product = $5,
               listed_DogDiet_MVP = $6, dogapi_id = $7
               WHERE {search_field} = $8""",
            data.breed_name_AKC,
            data.breed_group_AKC,
            data.breed_size_categ_AKC,
            data.breed_life_expect_yrs,
            data.food_recomm_product,
            data.listed_DogDiet_MVP,
            data.dogapi_id,
            search_value  # WHERE clause parameter
        )
        
        return {
            'success': True,
            'message': f'Breed fully replaced successfully via {search_field}',
            'search_value': search_value
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Server Entry Point ====================

# Main entry point - run the FastAPI server
if __name__ == '__main__':  # Only runs if script is executed directly (not imported as module)
    # Start uvicorn ASGI server (FastAPI runs on ASGI, not WSGI like Flask)
    # host='0.0.0.0' makes it accessible from other devices on network (not just localhost)
    # port=5000 is the server port (change if port conflict occurs)
    # reload=True enables auto-reload on code changes (disable in production for better performance)
    uvicorn.run(
        "main:app",  # Format: "filename:app_variable_name"
        host="0.0.0.0",
        port=5000,
        reload=True  # Automatically restart server when code changes detected
    )
