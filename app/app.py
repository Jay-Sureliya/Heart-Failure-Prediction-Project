import streamlit as st
import requests

# ---------- PAGE CONFIG (DARK MODE) ------------
st.set_page_config(
    page_title="HeartGuard AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM DARK CSS THEME ------------
st.markdown("""
<style>
    /* Global Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0a0f1f 0%, #111d33 100%);
        color: #e3e6ed !important;
    }

    /* Glass Card (Neon Glow Effect) */
    .glass-card {
        background: rgba(14, 22, 41, 0.55);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 18px;
        border: 1px solid rgba(0, 255, 200, 0.25);
        box-shadow: 0px 0px 18px rgba(0, 255, 200, 0.08);
        padding: 30px;
        margin-bottom: 18px;
    }

    /* Stylish Button - Neon Red */
    .stButton>button {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
        color: white;
        padding: 12px 28px;
        border-radius: 12px;
        border: none;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 22px rgba(255, 75, 43, 0.7);
    }

    /* Headings - Cyan Medical Neon */
    h1, h2, h3, h4 {
        color: #00e6b8 !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }

    /* Input Label Styling */
    .stNumberInput label, .stSelectbox label {
        color: #8fb7d9 !important;
        font-weight: 600;
        font-size: 14px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(11, 18, 32, 0.9);
        border-right: 1px solid rgba(0, 255, 200, 0.2);
    }

    .sidebar-content {
        color: #e8f1fb;
    }

    /* Info Box Color Fix */
    .stAlert {
        background-color: rgba(255,255,255,0.05) !important;
        color: #e8f1fb !important;
    }

</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=100)
    st.title("HeartGuard AI")
    st.caption("🔬 Advanced Cardiac Risk Prediction")

    st.markdown("---")
    st.subheader("💡 What It Does?")
    st.info("""
        This AI model analyzes **11 medical features**
        to predict **heart disease risk**.
    """)

    st.markdown("---")
    st.caption("👨‍⚕️ Made by Jay")


# ---------- MAIN CONTENT AREA ------------
col_spacer1, col_main, col_spacer2 = st.columns([1, 4, 1])

with col_main:
    st.markdown("<h1 style='text-align: center;'>🫀 Patient Assessment Form</h1>", unsafe_allow_html=True)


    with st.form("heart_form"):
        st.subheader("Basic information")

        # Row 1
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", 18, 100, 50)
        with c2:
            sex = st.selectbox("Sex", ["M", "F"])
        with c3:
            resting_bp = st.number_input("Resting BP (mm Hg)", 50, 250, 120)

        st.markdown("---")
        st.subheader("Cardiac Indicators")

        # Row 2
        c4, c5 = st.columns(2)
        with c4:
            chest_pain = st.selectbox("Chest Pain Type", ["ASY", "ATA", "NAP", "TA"])
            cholesterol = st.number_input("Cholesterol (mm/dl)", 0, 600, 200)
            fasting_bs = st.selectbox("Fasting Blood Sugar > 120?", [0, 1],
                                      format_func=lambda x: "Yes" if x == 1 else "No")
        with c5:
            max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
            exercise_angina = st.selectbox("Exercise Angina?", ["N", "Y"])
            st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

        # Row 3
        c6, c7 = st.columns(2)
        with c6:
            resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        with c7:
            oldpeak = st.number_input("Oldpeak (ST Depression)", -2.0, 6.0, 0.0, step=0.1)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍 Analyze Risk")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- RESULT SECTION ------------

if submitted:
    data = {
        "Age": age, "Sex": sex, "ChestPainType": chest_pain,
        "RestingBP": resting_bp, "Cholesterol": cholesterol,
        "FastingBS": fasting_bs, "RestingECG": resting_ecg,
        "MaxHR": max_hr, "ExerciseAngina": exercise_angina,
        "Oldpeak": oldpeak, "ST_Slope": st_slope
    }

    try:
        with st.spinner("Analyzing clinical data..."):
            response = requests.post("http://127.0.0.1:8000/predict", json=data)

        if response.status_code == 200:
            result = response.json()
            label = result["prediction"]
            prob = result["probability"]


            if label == "Heart Disease":
                st.error("⚠️ **HIGH RISK DETECTED**")
                st.markdown(f"<h3 style='color:#ff4b4b;'>Probability: {prob:.1%}</h3>", unsafe_allow_html=True)
                st.progress(prob)
                st.warning("👨‍⚕️ Recommendation: **Consult a cardiologist immediately.** Schedule ECG, TMT, and lipid tests.")
            else:
                st.success("✅ **LOW RISK / NORMAL**")
                st.markdown(f"<h3 style='color:#00e676;'>Risk Probability: {prob:.1%}</h3>", unsafe_allow_html=True)
                st.progress(prob)
                st.info("💙 Recommendation: Maintain a healthy lifestyle, exercise regularly & get annual checkups.")

        else:
            st.error("❌ Error: Could not connect to the API.")
    except Exception as e:
        st.error(f"🚨 Backend Error: {e}")
