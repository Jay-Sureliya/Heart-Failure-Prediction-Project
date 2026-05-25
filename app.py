import streamlit as st
import requests

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="❤️",
    layout="centered"
)

# 2. Header Section
st.title("❤️ Heart Disease Risk Assessment")
st.markdown("""
This application uses a machine learning model to predict the risk of heart disease based on standard patient vitals. 
Please fill out the form below.
""")
st.divider()

# URL of your FastAPI backend
API_URL = "https://heart-disease-api-x3wr.onrender.com/predict"

# 3. Use a form to prevent automatic page reloads on every input change
with st.form("patient_form"):
    st.subheader("Patient Details & Vitals")
    
    # Use columns for a clean layout
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=50, help="Age in years")
        resting_bp = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120, help="Resting blood pressure in mm Hg")
        cholesterol = st.number_input("Cholesterol", min_value=0, max_value=600, value=200, help="Serum cholesterol in mg/dl")
        max_hr = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150, help="Maximum heart rate achieved")

    with col2:
        oldpeak = st.number_input("Oldpeak", min_value=-2.0, max_value=6.0, value=0.0, step=0.1, help="ST depression induced by exercise relative to rest")
        st_slope = st.selectbox("ST Slope", ['Up', 'Flat', 'Down'], help="The slope of the peak exercise ST segment") 
        chest_pain = st.selectbox("Chest Pain Type", ['ATA', 'NAP', 'ASY', 'TA'])
        exercise_angina = st.selectbox("Exercise Angina", ['N', 'Y'], help="Exercise-induced angina")

    st.write("") # Add a little vertical space
    
    # The submit button
    submitted = st.form_submit_button("Predict Heart Disease Risk", type="primary", use_container_width=True)

# 4. Handle the prediction after the form is submitted
if submitted:
    # Package data for the API
    patient_data = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope,
        "ChestPainType": chest_pain,
        "ExerciseAngina": exercise_angina
    }
    
    with st.spinner("Analyzing patient data..."):
        try:
            # Send POST request to FastAPI
            response = requests.post(API_URL, json=patient_data)
            
            if response.status_code == 200:
                result = response.json()
                
                st.divider()
                st.subheader("Prediction Results")
                
                # Display Results beautifully
                res_col1, res_col2 = st.columns([2, 1])
                
                with res_col1:
                    if result["prediction"] == 1:
                        st.error(f"🚨 **{result['risk_status']}**")
                        st.markdown("It is highly recommended that this patient consults with a cardiologist for further evaluation.")
                    else:
                        st.success(f"✅ **{result['risk_status']}**")
                        st.markdown("The patient's vitals do not currently indicate a high risk of heart disease.")
                
                # Display the model's confidence as a sleek metric
                with res_col2:
                    confidence_pct = round(result['probability_score'] * 100, 1)
                    st.metric(label="Model Confidence", value=f"{confidence_pct}%")
                    
            else:
                st.error(f"Server Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ **Connection Error:** Could not connect to the API. Please ensure your FastAPI server is running in another terminal using `uvicorn main:app --reload`.")