import streamlit as st
import pandas as pd
import joblib
import os

# ---------- PAGE CONFIG ------------
st.set_page_config(page_title="HeartGuard AI", page_icon="🫀", layout="wide")

# ---------- LOAD MODEL ------------
# Using caching so it only loads the model once, making the app much faster
@st.cache_resource
def load_model():
    # Construct path relative to this script
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'heart_disease_pipeline.pkl')
    return joblib.load(model_path)

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Failed to load model: {e}. Did you run train_model.py first?")

# ---------- UI & FORM ------------
st.title("🫀 HeartGuard AI - Risk Assessment")
st.markdown("This AI analyzes 8 clinical features to predict heart disease risk.")

if model_loaded:
    with st.form("patient_form"):
        st.subheader("Patient Clinical Data")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", 18, 100, 50)
            resting_bp = st.number_input("Resting BP (mm Hg)", 50, 250, 120)
            cholesterol = st.number_input("Cholesterol (mm/dl)", 0, 600, 200)
            
        with c2:
            max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
            oldpeak = st.number_input("Oldpeak (ST Depression)", -2.0, 6.0, 0.0, step=0.1)
            
        with c3:
            chest_pain = st.selectbox("Chest Pain Type", ["ASY", "ATA", "NAP", "TA"])
            exercise_angina = st.selectbox("Exercise Angina?", ["N", "Y"])
            st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

        submitted = st.form_submit_button("🔍 Analyze Risk", use_container_width=True)

# ---------- PREDICTION LOGIC ------------
if submitted and model_loaded:
    # 1. Package the data exactly as the ColumnTransformer expects it
    input_data = pd.DataFrame({
        'Age': [age],
        'RestingBP': [resting_bp],
        'Cholesterol': [cholesterol],
        'MaxHR': [max_hr],
        'Oldpeak': [oldpeak],
        'ChestPainType': [chest_pain],
        'ExerciseAngina': [exercise_angina],
        'ST_Slope': [st_slope]
    })

    # 2. Run Inference
    with st.spinner("Analyzing..."):
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

    # 3. Display Results
    st.markdown("---")
    if prediction == 1:
        st.error("⚠️ **HIGH RISK DETECTED**")
        st.write(f"**Probability of Heart Disease:** {probability:.1%}")
        st.progress(float(probability))
        st.warning("Recommendation: Consult a cardiologist immediately.")
    else:
        st.success("✅ **LOW RISK / NORMAL**")
        st.write(f"**Probability of Heart Disease:** {probability:.1%}")
        st.progress(float(probability))
        st.info("Recommendation: Maintain a healthy lifestyle.")