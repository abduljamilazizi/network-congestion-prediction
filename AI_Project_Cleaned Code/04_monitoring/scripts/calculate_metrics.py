import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.models import load_model

RF_MODEL_PATH = "models/random_forest_model.pkl"
LSTM_MODEL_PATH = "models/lstm_model.h5"
LSTM_SCALER_PATH = "models/lstm_scaler.pkl"
BATCH_DATA_PATH = "data/new/new_data.csv"

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


def load_batch_data():
    df = pd.read_csv(BATCH_DATA_PATH)
    return df


def prepare_features_and_target(df):
    y = df["Label"].astype(int)
    X = df.drop(columns=["Label"])
    return X, y


def predict_rf(X):
    model = joblib.load(RF_MODEL_PATH)
    preds = model.predict(X)
    return np.array(preds).astype(int)


def predict_lstm(X):
    model = load_model(LSTM_MODEL_PATH)
    scaler = joblib.load(LSTM_SCALER_PATH)

    X_scaled = scaler.transform(X.to_numpy(dtype=np.float32))
    X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    raw_preds = model.predict(X_scaled, verbose=0)
    if raw_preds.ndim > 1 and raw_preds.shape[1] > 1:
        preds = np.argmax(raw_preds, axis=1)
    else:
        preds = (raw_preds > 0.5).astype(int).flatten()

    return np.array(preds).astype(int)


def insert_monitoring_metrics(conn, model_name, accuracy, precision, recall, f1, total_samples, benign_count, attack_count):
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO monitoring_metrics
            (run_time, model_name, accuracy, precision_score, recall_score, f1_score, total_samples, benign_count, attack_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
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
                '''
                INSERT INTO prediction_logs
                (run_time, model_name, prediction, label_name)
                VALUES (%s, %s, %s, %s)
                ''',
                (datetime.now(), model_name, int(pred), label_name),
            )
    conn.commit()


def evaluate_and_store(model_name, y_true, predictions):
    accuracy = float(accuracy_score(y_true, predictions))
    precision = float(precision_score(y_true, predictions, zero_division=0))
    recall = float(recall_score(y_true, predictions, zero_division=0))
    f1 = float(f1_score(y_true, predictions, zero_division=0))
    total_samples = len(predictions)
    benign_count = int((predictions == 0).sum())
    attack_count = int((predictions == 1).sum())

    conn = get_db_connection()

    insert_monitoring_metrics(
        conn,
        model_name,
        accuracy,
        precision,
        recall,
        f1,
        total_samples,
        benign_count,
        attack_count,
    )

    insert_prediction_logs(conn, model_name, predictions)
    conn.close()

    print(f"{model_name.upper()} Accuracy: {accuracy:.4f}")
    print(f"{model_name.upper()} Precision: {precision:.4f}")
    print(f"{model_name.upper()} Recall: {recall:.4f}")
    print(f"{model_name.upper()} F1 Score: {f1:.4f}")


def main():
    df = load_batch_data()
    X, y = prepare_features_and_target(df)

    rf_preds = predict_rf(X)
    evaluate_and_store("rf", y, rf_preds)

    lstm_preds = predict_lstm(X)
    evaluate_and_store("lstm", y, lstm_preds)


if __name__ == "__main__":
    main()