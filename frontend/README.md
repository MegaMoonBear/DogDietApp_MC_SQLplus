# WhiskerWorthy static frontend

Plain HTML, CSS, and JS pages serve the dog questionnaire and the team admin form. No build step is required.

## How to run

- Open `index.html` in a browser, or
- Serve the folder locally (for API calls) with any static server, e.g. `python -m http.server 5173` from this directory.

## API expectations

- Questionnaire POST: `/api/submit-dog-info`
- Admin update PATCH: `/api/breed/{search_field}/{search_value}`
