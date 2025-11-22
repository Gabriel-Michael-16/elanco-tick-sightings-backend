# elanco-tick-sightings-backend
Author: Gabriel Michael
Backend MVP for tick sighting analysis - technical task for Elanco SWE Internship

Ticks are becoming increasingly prevalent across the UK, carrying diseases like Lyme disease that affects thousands annually. This Minimum Viable Product (MVP) aims to provide a backend that loads, processes and analyses tick sighting data

This Backend:
    -> Imports and Cleans data from excel
        -> Normalising column names and data
        -> Converting dates to datetime objects
        -> Removes duplicate records
    -> Contains Search and Filtering Endpoints
        -> Filtering by date and location
    -> Contains Data reporting Endpoints
        -> Grouping by week or month
        -> Grouping by location
    -> Provides system health
        -> Verifying dataset is loaded and API is alive
    -> Handles Errors
        -> Validating date ranges
        -> Handling invalid formats
        -> Checks valid location requests
        -> Returns JSON errors
    -> Implements CORS support for Frontend Applications

Endpoint Documentation:
    -> GET /health
    -> GET /search?location=leicester*start_date=YYYY-MM-DD
    -> GET /reports/weekly
    -> GET /reports/monthly
    -> GET /reports/regions

Necessary Dependencies:
    -> fastapi
    -> uvicorn
    -> pandas
    -> openpyxl

Instructions to run:
    In terminal:
        Clone github repository using: 
            -> git clone https://github.com/Gabriel-Michael-16 elanco-tick-sightings-backend.git
            -> cd elanco-tick-sightings-backend
        Install dependencies:
            -> pip install -r requirements.txt
        Start FastAPI server:
            -> uvicorn main:app --reload
        Go to:
            -> http://127.0.0.1:8000/docs
        Stop server with:
            -> CTRL + C