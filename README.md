# WhiskerWorthy DogDietApp

A simplified dog diet application connecting pet owners with veterinary insights using AI.

## Project Goals
1.  **Collect User Responses**: Save responses from the 3-question form on the homepage to the database.
2.  **Connect to AI**: Use the "ViggoVet" dataset (HuggingFace) to provide context for AI responses.
3.  **Guide AI**: Generate 3 tailored questions for the veterinarian based on the user's input (Age, Health Status) and the ViggoVet dataset context.

## Repository Structure
-   **frontend/**: Static HTML/CSS/JS site.
-   **backend/**: FastAPI application with PostgreSQL database connection.

## Setup & Running

### 1. Backend
The backend is a FastAPI service running on port 5000.

```bash
cd backend
# Ensure virtual environment is active and dependencies installed
python main.py
```
-   **API Docs**: [http://localhost:5000/docs](http://localhost:5000/docs)

### 2. Frontend
The frontend is a static site. You can serve it using Python's http.server.

```bash
cd frontend
python -m http.server 5173
```
-   **App URL**: [http://localhost:5173](http://localhost:5173)

## Key API Endpoints
-   `POST /api/submit-dog-info`: Submit questionnaire data (Breed, Age, Health Status).
-   `POST /api/questions/ai`: Generate AI-driven questions for the vet.
-   `GET /api/breeds`: Retrieve breed list.

## Data Fields
-   **Questionnaire**: `breed_name_AKC`, `age_years_preReg`, `status_dietRelat_preReg` (multi-select).
-   **Breeds**: `breed_name_AKC`, `breed_group_AKC`, `breed_size_categ_AKC`, `breed_life_expect_yrs`.

## Environment
-   Backend requires a `.env` file with `DATABASE_URL` and `OPENAI_API_KEY`.
