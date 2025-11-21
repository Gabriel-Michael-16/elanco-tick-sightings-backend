import pandas as pd
from fastapi import FastAPI

def cleanTickData(dataSet):

    dataSet.columns = dataSet.columns.str.lower()
    dataSet["date"] = pd.to_datetime(dataSet["date"])
    
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

    
dataSet = loadExcelDataset(r'C:\Interview Code\Elanco data code\Tick Sightings.xlsx')

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Tick API is running"}

@app.get("/search")
def searchSightings(startDate: str = None, endDate: str = None, location: str = None):
    results = dataSet.copy()
    
print("Git push working")
