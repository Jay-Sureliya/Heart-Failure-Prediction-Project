# ❤️ HeartGuard AI - Heart Failure Prediction System

A full-stack machine learning application that predicts the likelihood of heart disease based on clinical parameters. The system uses a **Random Forest** model wrapped in a FastAPI backend and served via a modern Streamlit dashboard.

## 🚀 Features
- **Accurate Predictions:** Uses a Random Forest Classifier with ~84% accuracy.
- **Robust Pipeline:** Implements Scikit-Learn Pipelines for automated scaling, imputation, and encoding.
- **Dual Architecture:** Decoupled architecture with a FastAPI backend and Streamlit frontend.
- **Interactive UI:** Glassmorphism-styled dashboard with real-time risk probability visualization.

## 📂 Project Structure
```text
Heart_Failure_Prediction/
├── app/
│   ├── main.py          # FastAPI Backend (The Brain)
│   └── app.py           # Streamlit Frontend (The Interface)
├── data/
│   └── heart.csv        # Raw Dataset
├── model/
│   └── heart_disease_pipeline.pkl  # Trained Model Artifact
├── src/
│   └── train_model.py   # Script to train and save the model
├── requirements.txt     # Dependencies
└── README.md            # Project Documentation

🛠️ Tech Stack
Model: Python, Scikit-Learn (Random Forest), Pandas

Backend: FastAPI, Uvicorn, Pydantic

Frontend: Streamlit, Requests, CSS

Utilities: Joblib (Serialization)

⚙️ Installation & Setup
Clone the Repository

Bash

git clone <your-repo-url>
cd Heart_Failure_Prediction
Create a Virtual Environment (Optional but Recommended)

Bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Install Dependencies

Bash

pip install -r requirements.txt
Train the Model (Only needed if model/heart_disease_pipeline.pkl is missing)

Bash

python src/train_model.py
🏃‍♂️ How to Run
You need to run the Backend and Frontend in two separate terminals.

Terminal 1: Start the Backend (API)

Bash

uvicorn app.main:app --reload
The API will start at http://127.0.0.1:8000

Terminal 2: Start the Frontend (Dashboard)

Bash

streamlit run app/app.py
The Dashboard will open in your browser at http://localhost:8501

📊 Model Performance
The model was trained on the Heart Failure Prediction dataset.

Algorithm: Random Forest Classifier (Tuned)

Key Predictors: ST Slope, Chest Pain Type, Exercise Angina

Accuracy: ~84% on test data

Made with ❤️ by Jay Sureliya