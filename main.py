from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="An API that predicts heart disease risk based on patient vitals."
)

# 2. Load the trained model pipeline
try:
    model = joblib.load('model/heart_disease_pipeline.pkl')
except FileNotFoundError:
    model = None
    print("Warning: Model file not found. Ensure 'model/heart_disease_pipeline.pkl' exists.")

# 3. Define the exact 8 input features your model was trained on
class PatientData(BaseModel):
    Age: int = Field(..., example=50, description="Age of the patient")
    RestingBP: int = Field(..., example=120, description="Resting blood pressure")
    Cholesterol: int = Field(..., example=200, description="Serum cholesterol in mg/dl")
    MaxHR: int = Field(..., example=150, description="Maximum heart rate achieved")
    Oldpeak: float = Field(..., example=0.0, description="ST depression induced by exercise relative to rest")
    ST_Slope: str = Field(..., example="Up", description="The slope of the peak exercise ST segment (Up, Flat, Down)")
    ChestPainType: str = Field(..., example="ATA", description="Chest pain type (TA, ATA, NAP, ASY)")
    ExerciseAngina: str = Field(..., example="N", description="Exercise-induced angina (Y or N)")

# 4. Create the prediction endpoint
@app.post("/predict")
def predict_heart_disease(data: PatientData):
    if not model:
        raise HTTPException(status_code=500, detail="Machine learning model is not loaded on the server.")
    
    try:
        # Convert the incoming JSON payload into a Pandas DataFrame
        # The keys must perfectly match the columns in your training data
        input_df = pd.DataFrame([data.dict()])
        
        # Generate prediction (0 = Normal, 1 = Heart Disease)
        prediction = model.predict(input_df)
        
        # Get the probability (confidence score) of the prediction
        # predict_proba returns an array like [[prob_class_0, prob_class_1]]
        probability = model.predict_proba(input_df)[0][1] 
        
        # Format the response
        is_high_risk = bool(prediction[0] == 1)
        
        return {
            "prediction": int(prediction[0]),
            "risk_status": "High Risk of Heart Disease" if is_high_risk else "Low Risk of Heart Disease",
            "probability_score": round(float(probability), 4)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")

# 5. Add a simple health check route
@app.get("/")
def health_check():
    return {"status": "API is running. Send POST requests to /predict."}