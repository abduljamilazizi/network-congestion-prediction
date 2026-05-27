import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
mlflow.set_tracking_uri("file:///D:/MSITDS/Second Semester/AI_ML_Project/network-congestion-prediction/mlruns")

# Set experiment
mlflow.set_experiment("network_congestion_prediction")

print("Starting MLflow run...")

# Load dataset
data = pd.read_csv("data/processed/cleaned_network_data.csv")

data.columns = data.columns.str.strip()
data["Label"] = data["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# sample smaller dataset
data = data.sample(n=100000, random_state=42)

X = data.drop(columns=["Label"])
y = data["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

with mlflow.start_run():

    print("Training model...")

    model = RandomForestClassifier(
        n_estimators=20,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", accuracy)

    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("n_estimators", 20)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "model")

    joblib.dump(model, "models/random_forest_model.pkl")

    print("MLflow run completed and logged.")