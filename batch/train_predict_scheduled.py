from pathlib import Path
import csv
from datetime import datetime

import joblib
import pandas as pd
from prefect import flow, task

MODEL_PATH = Path("models/random_forest_model.pkl")
LOG_PATH = Path("logs/prefect_batch_predictions.csv")


@task
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


@task
def prepare_batch_input() -> pd.DataFrame:
    data = [
        {
            "Destination Port": 443,
            "Flow Duration": 120,
            "Total Fwd Packets": 10,
            "Total Backward Packets": 8,
            "Total Length of Fwd Packets": 1200,
            "Total Length of Bwd Packets": 900,
            "Fwd Packet Length Max": 300,
            "Fwd Packet Length Min": 50,
            "Fwd Packet Length Mean": 120,
            "Fwd Packet Length Std": 30,
        },
        {
            "Destination Port": 80,
            "Flow Duration": 200,
            "Total Fwd Packets": 20,
            "Total Backward Packets": 15,
            "Total Length of Fwd Packets": 1500,
            "Total Length of Bwd Packets": 1100,
            "Fwd Packet Length Max": 400,
            "Fwd Packet Length Min": 60,
            "Fwd Packet Length Mean": 140,
            "Fwd Packet Length Std": 35,
        },
    ]
    return pd.DataFrame(data)


@task
def predict_batch(model, batch_df: pd.DataFrame):
    batch_df.columns = batch_df.columns.str.strip()
    predictions = model.predict(batch_df)
    return predictions.tolist()


@task
def save_predictions(batch_df: pd.DataFrame, predictions: list):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "Destination_Port",
                    "Flow_Duration",
                    "Total_Fwd_Packets",
                    "Total_Backward_Packets",
                    "Total_Length_of_Fwd_Packets",
                    "Total_Length_of_Bwd_Packets",
                    "Fwd_Packet_Length_Max",
                    "Fwd_Packet_Length_Min",
                    "Fwd_Packet_Length_Mean",
                    "Fwd_Packet_Length_Std",
                    "prediction",
                ]
            )

        for row, pred in zip(batch_df.to_dict(orient="records"), predictions):
            writer.writerow(
                [
                    datetime.now().isoformat(),
                    row["Destination Port"],
                    row["Flow Duration"],
                    row["Total Fwd Packets"],
                    row["Total Backward Packets"],
                    row["Total Length of Fwd Packets"],
                    row["Total Length of Bwd Packets"],
                    row["Fwd Packet Length Max"],
                    row["Fwd Packet Length Min"],
                    row["Fwd Packet Length Mean"],
                    row["Fwd Packet Length Std"],
                    int(pred),
                ]
            )

    return str(LOG_PATH)


@flow(name="network_congestion_batch_predict")
def network_congestion_batch_predict():
    model = load_model()
    batch_df = prepare_batch_input()
    predictions = predict_batch(model, batch_df)
    output_path = save_predictions(batch_df, predictions)

    print("Batch prediction completed.")
    print("Predictions:", predictions)
    print("Saved to:", output_path)


if __name__ == "__main__":
    network_congestion_batch_predict()