-- Updated for WhiskerWorthy Phase 2 by adding AI to generate nutritional questions for veterinarian 

-- SQL code for creating table that will store DEVELOPER info on breeds to 3 initial dog questions
CREATE TABLE breedsAKC_IDs_v3 (
  breed_name_AKC TEXT PRIMARY KEY,  --see questions_home_dog_4Q_v2 table's "id" field
  breed_group_AKC_name TEXT, -- e.g. names for sporting, hound, working, terrier, toy, non-sporting, herding, misc
  breed_life_expect_yrs DECIMAL(3,1), -- 3 = total digits allowed, 1 = digits after decimal
    -- Last fields are INTERNAL-ONLY for now
  breed_size_categ_AKC TEXT, -- small, medium, large, or extra large based on AKC size categories 
  breed_size_VS_LifeSpan BINARY, -- Does size match lifespan data groupings?
  breed_categ_LifeSpan_Research TEXT, -- small, medium, large, or extra large based on lifespan data groupings
  breed_categ_LifeSpan_CrowdSource TEXT, -- small, medium, large, or extra large based on lifespan data groupings
      -- Last fields are INTERNAL-ONLY - Only for API lookup/reference - DogAPI.org
  breed_group_AKC_ID TEXT, -- e.g. IDs for sporting, hound, working, terrier, toy, non-sporting, herding, misc
  dogapi_id TEXT --INTERNAL-ONLY 35-character ID for KEY in dog information database, DogAPI.org
);
INSERT INTO breedsAKC_IDs_v3 (breed_name_AKC, dogapi_id)
VALUES ('Labrador Retriever', 'dogapi_0123456789abcdef012345678901234');

-- SQL code for creating table that will collect user responses to 3 initial dog questions
CREATE TABLE questions_home_dog_4Q_v2 (
  id_dog_preRegis SERIAL PRIMARY KEY,  -- Automatically assigned (SERIAL) as KEY for questions_home_dog_4Q_v2 table's "id" field
  breed_name_AKC_preRegis TEXT,  -- see questions_home_dog_4Q_v2 table's "Breed (name)" field
  age_years_preReg DECIMAL(3,2), -- 3 = total digits allowed, 2 = digits after decimal; -- see questions_home_dog_4Q_v2 table's "Age (years)" field
  status_dietRelat_preReg TEXT, -- none, puppy, elderly, pregnant, allergy, "Other health issues"
  zipcode_preReg TEXT,  -- User's ZIP code (to help tailor recommendations by region/climate if needed in future)
  DateTime_preReg TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automated current date/time when record created (to handle dups from registration; not modified, since User updates in different form/table)
  -- update DateTime to include time zone: TIMESTAMP **WITH TIME ZONE** DEFAULT CURRENT_TIMESTAMP
  );  
 
--  NOTES ON VARIABLES TO ADD LATER:

-- dietRelated status details (to expand later):
  -- status_dietRelated -- INTERNAL VARIABLE NAME: noneV1, puppy, elderly, pregnant, allergy, OtherHealthV1
  -- status_dietRelated: Possible updates: None observed vs. Vet-confirmed with appointment in last 12 months; puppy by age (milk-only, transition/softer, puppy but adult format (dry, etc.)), elder stages: _, pregnant: _, 
  -- status_dietRelated: allergy: environmental, diet, or possible; "Other health issues" 
  -- status_dietRelated: overweight, underweight, healthy weight)
  -- status_dietRelated: weight, picture-based assessment, or vet-confirmed?

-- weight-related details (to expand later):
  -- Weight is relatively simple metric, but the follow-up questions to determine if overweight/underweight/healthy weight is COMPLEX
    -- weight_units -- lbs vs. kgs?
    -- weight_lbs DECIMAL(5,2)  -- 5 = total digits allowed, 2 = digits after decimal 
    -- weight_status_APP TEXT,  -- e.g., underweight, healthy weight, overweight 
    -- weight_by_age_percentile_APP -- e.g., 10th, 25th,
      --   -- Last 4 of 12 fields are INTERNAL-ONLY
      --   -- weight_by_age_percentile_RSRCH -- e.g., 10th, 25th,

  -- -- SQL code for creating table that will store DEVELOPER info on breeds to 3 initial dog questions
  -- CREATE TABLE breeds_AKC_Rsrch_FoodV2 (
  --   breed_otherNames TEXT, -- separate multiple names with semicolon
  --   listed_DogDiet_MVP CHAR(1),  -- Y/N  /* Yes as "Y" for limited breeds for initial MVP/phases */
  --   food_recomm_brand TEXT,  -- e.g., Nutri-Source, Blue Buffalo, Hill's Science Diet
  --   food_recomm_product TEXT, -- e.g., Fromm Gold Large Breed Adult Kibble
  --   food_recomm_format TEXT, -- e.g., kibble, wet, raw
  --   -- Last 4 of 12 fields are INTERNAL-ONLY
  --   food_rec_note_INTERNAL TEXT,
  --   dogapi_id TEXT SECONDARY KEY --INTERNAL-ONLY 35-character ID, used to look up this breed in the dog information database, DogAPI.org
  -- );
