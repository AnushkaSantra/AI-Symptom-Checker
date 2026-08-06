import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/disease_model.pkl")

# Load dataset to get symptom names
df = pd.read_csv("dataset/Training.csv")

# Remove extra column
if "Unnamed: 133" in df.columns:
    df = df.drop(columns=["Unnamed: 133"])

# Get symptom column names
symptoms = list(df.columns[:-1])

# Create empty input (all symptoms absent)
input_data = [0] * len(symptoms)

# Example: Patient has itching and skin_rash
input_data[symptoms.index("itching")] = 1
input_data[symptoms.index("skin_rash")] = 1

# Predict disease
prediction = model.predict([input_data])

print("Predicted Disease:", prediction[0])