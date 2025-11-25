
-- SQL code for creating table that will store DEVELOPER info on breeds to 3 initial dog questions
CREATE TABLE breeds_AKC_Rsrch_FoodV1 (
  breed_name_AKC TEXT PRIMARY KEY,  --see questions_dog_initial3 table's "id" field
  breed_group_AKC TEXT, -- e.g., sporting, hound, working, terrier, toy, non-sporting, herding, misc
  breed_life_expect_yrs DECIMAL(3,1), -- 3 = total digits allowed, 1 = digits after decimal
  listed_DogDiet_MVP CHAR(1),  -- Y/N  /* Yes as "Y" for limited breeds for initial MVP/phases */
  food_recomm_product TEXT, -- e.g., Fromm Gold Large Breed Adult Kibble
  -- Last of 6 fields are INTERNAL-ONLY
  dogapi_id TEXT --INTERNAL-ONLY 35-character ID, used to look up this breed in the dog information database, DogAPI.org
);
  -- -- SQL code for creating table that will store DEVELOPER info on breeds to 3 initial dog questions
  -- CREATE TABLE breeds_AKC_Rsrch_FoodV2 (
  --   breed_name_AKC TEXT PRIMARY KEY,  --see questions_dog_initial3 table's "id" field
  --   breed_otherNames TEXT, -- separate multiple names with semicolon
  --   breed_group_AKC TEXT, -- e.g., sporting, hound, working, terrier, toy, non-sporting, herding, misc
  --   breed_size_categ_AKC -- small, medium, large, or extra large based on AKC size categories.
  --   breed_life_expect_yrs DECIMAL(3,1), -- 3 = total digits allowed, 1 = digits after decimal
  --   listed_DogDiet_MVP CHAR(1),  -- Y/N  /* Yes as "Y" for limited breeds for initial MVP/phases */
  --   food_recomm_brand TEXT,  -- e.g., Nutri-Source, Blue Buffalo, Hill's Science Diet
  --   food_recomm_product TEXT, -- e.g., Fromm Gold Large Breed Adult Kibble
  --   food_recomm_format TEXT, -- e.g., kibble, wet, raw
  --   -- Last 4 of 12 fields are INTERNAL-ONLY
  --   food_rec_note_INTERNAL TEXT,
  --   size_category TEXT,  -- INTERNAL-ONLY e.g., toy?, small, medium, large, extra large? see AKC size categories
  --   breed_class_AKC TEXT,  -- INTERNAL-ONLY recognized, Foundation Stock Service (FSS), or Miscellaneous 
  --   dogapi_id TEXT SECONDARY KEY --INTERNAL-ONLY 35-character ID, used to look up this breed in the dog information database, DogAPI.org
  -- );
  --     -- weight_by_age_percentile_RSRCH -- e.g., 10th, 25th,


-- SQL code for creating table that will collect user responses to 3 initial dog questions
CREATE TABLE questions_dog_initial3 (
  id_dog_preRegis SERIAL PRIMARY KEY,  -- Automatically assigned (SERIAL) as KEY for questions_dog_initial3 table's "id" field
  breed_name_AKC TEXT,  -- see questions_dog_initial3 table's "Breed (name)" field
  age_years_preReg DECIMAL(3,1), -- 3 = total digits allowed, 1 = digits after decimal; -- see questions_dog_initial3 table's "Age (years)" field
  status_dietRelat_preReg TEXT, -- none, puppy, elderly, pregnant, allergy, "Other health issues"
  modified_preReg TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automated current date/time when record created (to handle dups from registration; not modified, since User updates in different form/table)
  );  
 
  -- status_dietRelated -- INTERNAL VARIABLE NAME: noneV1, puppy, elderly, pregnant, allergy, OtherHealthV1
  -- status_dietRelated: Possible updates: None observed vs. Vet-confirmed with appointment in last 12 months; puppy by age (milk-only, transition/softer, puppy but adult format (dry, etc.)), elder stages: _, pregnant: _, 
  -- status_dietRelated: allergy: environmental, diet, or possible; "Other health issues" 
  -- status_dietRelated: overweight, underweight, healthy weight)
  -- status_dietRelated: weight, picture-based assessment, or vet-confirmed?

  -- Weight is relatively simple metric, but the follow-up questions to determine if overweight/underweight/healthy weight is COMPLEX
    -- weight_units -- lbs vs. kgs?
    -- weight_lbs DECIMAL(5,2)  -- 5 = total digits allowed, 2 = digits after decimal 
    -- weight_by_age_percentile_APP -- e.g., 10th, 25th,
    -- weight_status_APP TEXT,  -- e.g., underweight, healthy weight, overweight 






