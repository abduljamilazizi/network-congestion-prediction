import os
import joblib
import mlflow
import mlflow.sklearn
import mlflow.keras
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler

from tensorflow import keras


DATA_PATH = "data/processed/cleaned_network_data.csv"
MODELS_DIR = "models"

os.makedirs(MODELS_DIR, exist_ok=True)

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

print("Loading real CICIDS2017 cleaned dataset...")
df = pd.read_csv(DATA_PATH, low_memory=False)
df.columns = df.columns.str.strip()

df = df[selected_features + ["Label"]]
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# Sample for faster experiment tracking
df = df.sample(n=100000, random_state=42)

X = df[selected_features]
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

mlflow.set_experiment("network_congestion_prediction")


# =========================
# Random Forest Experiment
# =========================
with mlflow.start_run(run_name="Random_Forest_Real_Data"):
    print("Training Random Forest on real data...")

    rf_model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
        n_jobs=-1
    )

    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)

    mlflow.log_param("dataset", "CICIDS2017 cleaned dataset")
    mlflow.log_param("model_type", "Random Forest")
    mlflow.log_param("n_estimators", 50)
    mlflow.log_param("sample_size", 100000)

    mlflow.log_metric("accuracy", rf_accuracy)

    mlflow.sklearn.log_model(rf_model, "random_forest_model")

    joblib.dump(rf_model, "models/random_forest_model.pkl")

    print("Random Forest Accuracy:", rf_accuracy)


# =========================
# LSTM Experiment
# =========================
print("Preparing LSTM data...")

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

X_train_lstm, X_test_lstm, y_train_lstm, y_test_lstm = train_test_split(
    X_lstm, y, test_size=0.2, random_state=42, stratify=y
)

with mlflow.start_run(run_name="LSTM_Real_Data"):
    print("Training LSTM on real data...")

    lstm_model = keras.Sequential([
        keras.layers.LSTM(64, input_shape=(1, X.shape[1])),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid")
    ])

    lstm_model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    lstm_model.fit(
        X_train_lstm,
        y_train_lstm,
        epochs=5,
        batch_size=64,
        validation_split=0.2,
        verbose=1
    )

    loss, lstm_accuracy = lstm_model.evaluate(
        X_test_lstm,
        y_test_lstm,
        verbose=0
    )

    mlflow.log_param("dataset", "CICIDS2017 cleaned dataset")
    mlflow.log_param("model_type", "LSTM")
    mlflow.log_param("epochs", 5)
    mlflow.log_param("batch_size", 64)
    mlflow.log_param("sample_size", 100000)

    mlflow.log_metric("accuracy", lstm_accuracy)

    mlflow.keras.log_model(lstm_model, "lstm_model")

    lstm_model.save("models/lstm_model.h5")
    joblib.dump(scaler, "models/lstm_scaler.pkl")

    print("LSTM Accuracy:", lstm_accuracy)


# =========================
# Best Model Decision
# =========================
if rf_accuracy >= lstm_accuracy:
    best_model = "Random Forest"
    best_accuracy = rf_accuracy
else:
    best_model = "LSTM"
    best_accuracy = lstm_accuracy

with open("models/best_model_from_mlflow.txt", "w") as f:
    f.write(f"Best Model: {best_model}\n")
    f.write(f"Accuracy: {best_accuracy}\n")
    f.write("Dataset: CICIDS2017 cleaned dataset\n")

print("\nExperiments completed.")
print("Random Forest Accuracy:", rf_accuracy)
print("LSTM Accuracy:", lstm_accuracy)
print("Best Model:", best_model)