import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
import joblib

df = pd.read_csv('data/heart.csv')

# Feature groups
features_to_impute_and_scale = ['RestingBP', 'Cholesterol']
features_to_scale_only = ['Age', 'MaxHR', 'Oldpeak']
categorical_features = ['ST_Slope', 'ChestPainType']
ordinal_features = ['ExerciseAngina']

# Preprocessing pipelines
impute_scale_pipeline = Pipeline([
    ('imputer', SimpleImputer(missing_values=0, strategy='median')),
    ('scaler', StandardScaler())
])

scale_pipeline = Pipeline([
    ('scaler', StandardScaler())
])

ohe_transformer = OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False)
ord_transformer = OrdinalEncoder(categories=[['N', 'Y']])

# Combine preprocessing
preprocessor = ColumnTransformer([
    ('imp_scale', impute_scale_pipeline, features_to_impute_and_scale),
    ('scale', scale_pipeline, features_to_scale_only),
    ('ohe', ohe_transformer, categorical_features),
    ('ord', ord_transformer, ordinal_features)
], remainder='drop')

# Final model pipeline
model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(max_depth=30, min_samples_leaf=2,
                                          min_samples_split=10, n_estimators=100,
                                          random_state=42))
])

# Train-test split
X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_pipeline.fit(X_train, y_train)

print("Accuracy:", model_pipeline.score(X_test, y_test))

joblib.dump(model_pipeline, 'model/heart_disease_pipeline.pkl')
print("Model saved successfully.")