# WhiskerWorthy DogDietApp
Static HTML/CSS/JS frontend + FastAPI backend for dog diet intake and admin updates.

**Project goals** (*Ultimate goal: Improve understanding of pet nutrition for pet owners, veterinarians, and researchers*)
1) Save responses from 3 questions (homepage) to database table
2) Update breed-ID table with breed-group IDs and names for API communication
3) Display 3 preset veterinarian questions tailored to user responses 
4) Generate 3 questions for veterinarian with AI (*Ultimate goal*)
5) PRepare to collect initial crowd-sourced data for AI analyses 
______ Ensure the breed IDs table (breedsAKC_IDs_v3) is the source for the drop-down breed list in the first question. (((___))) For the breed IDs table - breedsAKC_IDs_v3, create IF...ELSE syntax in response to user responses to 1st and 3rd questions from ___ Based on the responses to first and third questions, show 3 pre-set questions from the ((())) a SQL script that creates a table and loads data and a python script that uses the created DB ((())) breed-ID table ((())) GET /api/questions/preset — returns up to three preset vet questions, lightly tailored by query params (breed_name_AKC, age_years_preReg, status_dietRelat_preReg[]). Uses `questions_home_dog_4Q_v2` as the storage table for collected responses.
POST /api/questions/ai — returns three placeholder AI-style questions based on the questionnaire payload; includes a TODO for real LLM integration. ((())) Add inline comments about any syntax lines that are ciritical or initial uses in each file related to yesterday's or today's changes.

## Layout
- frontend/ — static site (index.html, public/style.css, public/main.js, assets)
- backend/ — FastAPI (main.py), schemas/, models/, services/

## Run locally
1) Backend: `cd backend && python main.py` (serves http://localhost:5000, docs at /docs)
2) Frontend: `cd frontend && python -m http.server 5173` (open http://localhost:5173)

## Core API
- POST /api/submit-dog-info (breed, age, statuses)
- PATCH /api/breed/{search_field}/{search_value}
- GET /api/breeds and GET /api/breed/{search_field}/{search_value}

## Data fields (public)
- breeds: breed_name_AKC, breed_otherNames, breed_group_AKC, breed_size_categ_AKC, breed_life_expect_yrs, listed_DogDiet_MVP, food_recomm_brand/product/format
- questionnaire: breed_name_AKC, age_years_preReg, status_dietRelat_preReg

## Quick checks
- `python test_connections.py` validates backend, DB, and static server reachability.
- No Node/Vite build needed; serve static files over HTTP for fetch() calls.
