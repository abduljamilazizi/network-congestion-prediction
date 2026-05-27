import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load cleaned dataset
data = pd.read_csv("data/processed/cleaned_network_data.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Convert label column to numeric
data["Label"] = data["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# Keep only the 10 features used by the API
selected_features = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Fwd Packet Length Std",
]

# Use only selected columns + target
data = data[selected_features + ["Label"]]

# Faster development sample
data = data.sample(n=100000, random_state=42)

X = data[selected_features]
y = data["Label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/random_forest_model.pkl")
print("API-compatible model saved to models/random_forest_model.pkl")