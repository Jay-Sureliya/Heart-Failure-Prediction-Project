from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load the single pipeline file
model = joblib.load('heart_disease_pipeline.pkl')

# Define the data format (matches the CSV columns)
class PatientData(BaseModel):
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str

@app.post("/predict")
def predict_heart_disease(data: PatientData):
    # Convert incoming JSON to DataFrame
    df = pd.DataFrame([data.dict()])
    
    # Make Prediction
    prediction = model.predict(df)
    probability = model.predict_proba(df)
    
    result = "Heart Disease" if prediction[0] == 1 else "Normal"
    
    return {
        "prediction": result,
        "probability": float(probability[0][1])
    }