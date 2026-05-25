from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="HeartGuard API")

# Load the single pipeline file
# (If this file is missing, the API will crash on startup)
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

# --- NEW: Health Check Endpoint ---
@app.get("/")
def health_check():
    """This allows you to visit the API URL in your browser to see if it's awake."""
    return {
        "status": "Online", 
        "message": "HeartGuard API is running perfectly! Send POST requests to /predict."
    }

@app.post("/predict")
def predict_heart_disease(data: PatientData):
    try:
        # Convert incoming JSON to DataFrame
        # UPDATED: model_dump() is the modern replacement for the deprecated dict()
        df = pd.DataFrame([data.model_dump()])
        
        # Make Prediction
        prediction = model.predict(df)
        probability = model.predict_proba(df)
        
        result = "Heart Disease" if prediction[0] == 1 else "Normal"
        
        return {
            "prediction": result,
            "probability": float(probability[0][1])
        }
    except Exception as e:
        # If the model fails to process the data, return a clean error
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")