import pandas as pd

# Load dataset
df = pd.read_csv("dataset/Training.csv")

# Remove unwanted column
if "Unnamed: 133" in df.columns:
    df = df.drop(columns=["Unnamed: 133"])

# Split data
X = df.drop("prognosis", axis=1)
y = df["prognosis"]

print("Symptoms (X):")
print(X.head())

print("\nDiseases (y):")
print(y.head())