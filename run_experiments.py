import mlflow
import mlflow.sklearn
import mlflow.keras
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from tensorflow import keras

# Create dummy dataset (for demo if real dataset not used)
X, y = make_classification(n_samples=1000, n_features=10)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

mlflow.set_experiment("network_congestion_prediction")

# =========================
# 🔹 Experiment 1: Random Forest
# =========================
with mlflow.start_run(run_name="Random_Forest"):
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    accuracy = rf.score(X_test, y_test)

    mlflow.log_param("model", "RandomForest")
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(rf, "model")

# =========================
# 🔹 Experiment 2: LSTM
# =========================
X_train_lstm = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_lstm = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

with mlflow.start_run(run_name="LSTM"):
    model = keras.Sequential([
        keras.layers.LSTM(32, input_shape=(1, X_train.shape[1])),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train_lstm, y_train, epochs=3, verbose=0)

    loss, acc = model.evaluate(X_test_lstm, y_test, verbose=0)

    mlflow.log_param("model", "LSTM")
    mlflow.log_metric("accuracy", acc)

    mlflow.keras.log_model(model, "model")