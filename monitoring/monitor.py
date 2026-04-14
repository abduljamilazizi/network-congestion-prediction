import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.models import load_model


RF_MODEL_PATH = "models/random_forest_model.pkl"
LSTM_MODEL_PATH = "models/lstm_model.h5"
LSTM_SCALER_PATH = "models/lstm_scaler.pkl"
NEW_DATA_PATH = "data/new/new_data.csv"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoring_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def load_new_data():
    if not os.path.exists(NEW_DATA_PATH):
        raise FileNotFoundError(f"New data file not found: {NEW_DATA_PATH}")
    return pd.read_csv(NEW_DATA_PATH)


def prepare_features_and_target(df: pd.DataFrame):
    target_col = None
    for col in ["Label", "label", "target", "Target"]:
        if col in df.columns:
            target_col = col
            break

    if target_col:
        y_true = df[target_col]
        X = df.drop(columns=[target_col])
    else:
        y_true = None
        X = df.copy()

    return X, y_true


def normalize_labels(y_series: pd.Series):
    if y_series is None:
        return None

    mapping = {
        "BENIGN": 0,
        "benign": 0,
        "ATTACK": 1,
        "attack": 1,
        "MALICIOUS": 1,
        "malicious": 1,
    }

    if y_series.dtype == object:
        return y_series.map(lambda x: mapping.get(x, x))
    return y_series.astype(int)


def load_selected_model(model_type: str):
    model_type = model_type.lower()

    if model_type == "rf":
        return joblib.load(RF_MODEL_PATH)

    if model_type == "lstm":
        return load_model(LSTM_MODEL_PATH)

    raise ValueError("Invalid model type. Use 'rf' or 'lstm'.")


def predict_with_model(model, model_type: str, X: pd.DataFrame):
    model_type = model_type.lower()

    if model_type == "rf":
        predictions = model.predict(X)
        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)
        return np.array(predictions).astype(int), probabilities

    if model_type == "lstm":
        scaler = joblib.load(LSTM_SCALER_PATH)
        X_array = scaler.transform(X.to_numpy(dtype=np.float32))
        X_array = np.array(X_array, dtype=np.float32)
        X_array = X_array.reshape((X_array.shape[0], 1, X_array.shape[1]))

        raw_preds = model.predict(X_array, verbose=0)

        if raw_preds.ndim > 1 and raw_preds.shape[1] > 1:
            predictions = np.argmax(raw_preds, axis=1)
            probabilities = raw_preds
        else:
            predictions = (raw_preds > 0.5).astype(int).flatten()
            probabilities = raw_preds

        return np.array(predictions).astype(int), probabilities

    raise ValueError("Invalid model type. Use 'rf' or 'lstm'.")


def insert_monitoring_metrics(conn, model_name, accuracy, precision, recall, f1, total_samples, benign_count, attack_count):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO monitoring_metrics
            (run_time, model_name, accuracy, precision_score, recall_score, f1_score, total_samples, benign_count, attack_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                datetime.now(),
                model_name,
                accuracy,
                precision,
                recall,
                f1,
                total_samples,
                benign_count,
                attack_count,
            ),
        )
    conn.commit()


def insert_prediction_logs(conn, model_name, predictions):
    with conn.cursor() as cur:
        for pred in predictions:
            label_name = "BENIGN" if int(pred) == 0 else "ATTACK"
            cur.execute(
                """
                INSERT INTO prediction_logs
                (run_time, model_name, prediction, label_name)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    datetime.now(),
                    model_name,
                    int(pred),
                    label_name,
                ),
            )
    conn.commit()


def run_monitoring(model_type: str):
    print(f"\nRunning monitoring for model: {model_type}")

    model = load_selected_model(model_type)
    df = load_new_data()

    X, y_true = prepare_features_and_target(df)
    predictions, probabilities = predict_with_model(model, model_type, X)

    benign_count = int((predictions == 0).sum())
    attack_count = int((predictions == 1).sum())
    total_samples = len(predictions)

    print(f"{model_type.upper()} Predictions: {predictions.tolist()}")
    print(f"{model_type.upper()} Benign count: {benign_count}")
    print(f"{model_type.upper()} Attack count: {attack_count}")

    if probabilities is not None:
        print(f"{model_type.upper()} Raw probabilities/output:")
        print(probabilities)

    accuracy = None
    precision = None
    recall = None
    f1 = None

    if y_true is not None:
        y_true = normalize_labels(y_true)

        accuracy = float(accuracy_score(y_true, predictions))
        precision = float(precision_score(y_true, predictions, zero_division=0))
        recall = float(recall_score(y_true, predictions, zero_division=0))
        f1 = float(f1_score(y_true, predictions, zero_division=0))

        cm = confusion_matrix(y_true, predictions)
        print(f"{model_type.upper()} Confusion Matrix:\n{cm}")
        print(f"{model_type.upper()} Accuracy: {accuracy:.4f}")
        print(f"{model_type.upper()} Precision: {precision:.4f}")
        print(f"{model_type.upper()} Recall: {recall:.4f}")
        print(f"{model_type.upper()} F1 Score: {f1:.4f}")
    else:
        print("No label column found. Only class counts and predictions will be stored.")

    conn = get_db_connection()

    insert_monitoring_metrics(
        conn=conn,
        model_name=model_type.lower(),
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        total_samples=total_samples,
        benign_count=benign_count,
        attack_count=attack_count,
    )

    insert_prediction_logs(conn, model_type.lower(), predictions)

    conn.close()
    print(f"Monitoring completed for {model_type}.")


def main():
    run_monitoring("rf")
    run_monitoring("lstm")


if __name__ == "__main__":
    main()