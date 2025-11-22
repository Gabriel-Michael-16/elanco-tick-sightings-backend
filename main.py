import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

def cleanTickData(dataSet):

    dataSet.columns = dataSet.columns.str.lower()
    dataSet["date"] = pd.to_datetime(dataSet["date"])
    
    requiredColumns = ["id", "date", "location"]
    missing = [col for col in requiredColumns if col not in dataSet.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    
    stringColumns = ["species", "location", "latinname"]
    
    dataSet["year"] = dataSet["date"].dt.year
    dataSet["month"] = dataSet["date"].dt.month

    for column in stringColumns:
        if column in dataSet.columns:
            dataSet[column] = dataSet[column].astype(str).str.strip().str.lower()

    dataSet.drop_duplicates(subset=["id"], keep="first")

    return dataSet

def loadExcelDataset(path):
    rawData = pd.read_excel(path)
    return cleanTickData(rawData)

    
dataSet = loadExcelDataset(r'C:\Interview Code\Elanco data code\tickdata\Tick Sightings.xlsx')

def parseDate(dateStr: str):
    try:
        return pd.to_datetime(dateStr)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid date format: '{dateStr}'. Expected format: YYYY-MM-DD."
        )

app = FastAPI()

@app.exception_handler(Exception)
def allExceptionHandler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
                "error": "Internal server error",
                "details": str(exc)
                }
    )

@app.get("/")
def home():
    return {"message": "Tick API is running"}

@app.get("/search")
def searchSightings(
    startDate: str = None, 
    endDate: str = None, 
    location: str = None,
    page: int = 1,
    pageSize: int = 50
):
    results = dataSet.copy()
    
    if startDate:
        results = results[results["date"] >= parseDate(startDate)]
    
    if endDate:
        results = results[results["date"] <= parseDate(endDate)]

    if location and location not in dataSet["location"].unique():
        raise HTTPException(
            status_code=404,
            detail=f"Location '{location}' does not exist in dataset"
        )
    elif location:
        results = results[results["location"].str.contains(location.lower(), na=False)]
    
    results = results.sort_values(by="date", ascending=True)
    
    startIndex = (page-1)*pageSize
    endIndex = startIndex+pageSize

    paginated = results.iloc[startIndex:endIndex]
    
    return {
        "page": page,
        "pageSize": pageSize,
        "totalResults": len(results),
        "returnedResults": len(paginated),
        "data": paginated.to_dict(orient="records")} or {"message": "No sightings match search criteria", "data":[]}

@app.get("/reports/location")
def locationReport():
    group = dataSet.groupby("location").size().reset_index(name="count")
    return group.to_dict(orient="records")

@app.get("/reports/monthly")
def monthlyReport():
    group = dataSet.groupby("month").size().reset_index(name="count")
    return group.to_dict()

@app.get("/reports/weekly")
def weeklyReport():
    weekly = dataSet.copy()
    weekly["week"] = weekly["date"].dt.isocalendar().week
    
    group = weekly.groupby("week").size().reset_index(name="count")
    group = group.sort_values(by="week", ascending=True)

    return group.to_dict(orient="records")

