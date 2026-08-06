import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("dataset/Training.csv")

# Remove empty column if present
if "Unnamed: 133" in df.columns:
    df = df.drop(columns=["Unnamed: 133"])

# Split features and target
X = df.drop("prognosis", axis=1)
y = df["prognosis"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create the model
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Check accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Save the trained model
joblib.dump(model, "models/disease_model.pkl")

print("Model saved successfully!")