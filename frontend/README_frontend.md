# Frontend (static)

Plain HTML/CSS/JS, no build step. Entry: index.html loading public/style.css and public/main.js.

## Run
- Serve locally for API calls: `python -m http.server 5173` (from this folder)
- Open http://localhost:5173

## Forms & API
- Questionnaire form → POST /api/submit-dog-info (fields: breed_name_AKC, age_years_preReg, status_dietRelat_preReg[])
- Admin form → PATCH /api/breed/{search_field}/{search_value} (e.g., breed_name_AKC or dogapi_id)
- GET endpoints also available: /api/breeds and /api/breed/{search_field}/{search_value}

## Data field labels
- Breed table (public): breed_name_AKC, breed_otherNames, breed_group_AKC, breed_size_categ_AKC, breed_life_expect_yrs, listed_DogDiet_MVP, food_recomm_brand/product/format
- Questionnaire: breed_name_AKC, age_years_preReg, status_dietRelat_preReg (multi-select)

## Tips
- Use HTTP (not file://) so fetch works.
- CORS is open on the backend; no extra config needed.
