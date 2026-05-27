import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load cleaned dataset
data = pd.read_csv("data/processed/cleaned_network_data.csv")

print("Full dataset loaded:", data.shape)

# Clean column names
data.columns = data.columns.str.strip()

# Convert label column to numeric
data["Label"] = data["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# Faster development mode: sample smaller data
sample_size = 100000
data = data.sample(n=sample_size, random_state=42)

print("Sampled dataset shape:", data.shape)

# Separate features and target
X = data.drop(columns=["Label"])
y = data["Label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training samples:", X_train.shape)
print("Testing samples:", X_test.shape)

# Faster Random Forest
model = RandomForestClassifier(
    n_estimators=20,      # lower while testing
    random_state=42,
    n_jobs=-1             # use all CPU cores
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nModel Evaluation:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/random_forest_model.pkl")
print("Model saved to models/random_forest_model.pkl")