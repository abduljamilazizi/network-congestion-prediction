import os
from datetime import datetime
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Paths (keep your original ones)
MODEL_PATH = "models/random_forest_model.pkl"
NEW_DATA_PATH = "04_monitoring/data/current_batches/new_data.csv"

# Database config
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

def main():
    print("Running FULL monitoring with Switzerland timezone...")

    # Load model
    model = joblib.load(MODEL_PATH)

    # Load data
    df = pd.read_csv(NEW_DATA_PATH)
    df.columns = df.columns.str.strip()

    # Separate features and label
    if "Label" not in df.columns:
        print("Label column missing")
        return

    X = df.drop(columns=["Label"])
    y_true = df["Label"]

    # Predict
    y_pred = model.predict(X)

    # Metrics
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    # Switzerland timezone
    current_time = datetime.now(ZoneInfo("Europe/Zurich"))

    # DB insert
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS monitoring_metrics (
            id SERIAL PRIMARY KEY,
            accuracy FLOAT,
            precision FLOAT,
            recall FLOAT,
            f1_score FLOAT,
            timestamp TIMESTAMP WITH TIME ZONE
        )
        """
    )

    cur.execute(
        "INSERT INTO monitoring_metrics (accuracy, precision, recall, f1_score, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (acc, prec, rec, f1, current_time)
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted metrics at {current_time}")
    print(f"Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1: {f1}")

if __name__ == "__main__":
    main()
