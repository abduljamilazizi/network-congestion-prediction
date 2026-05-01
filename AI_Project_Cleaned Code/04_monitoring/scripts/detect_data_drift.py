import os
from datetime import datetime

import pandas as pd
import psycopg2

REFERENCE_PATH = "data/reference/reference_data.csv"
BATCH_PATH = "data/new/new_data.csv"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoring_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

FEATURES = [
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


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def main():
    reference_df = pd.read_csv(REFERENCE_PATH)
    batch_df = pd.read_csv(BATCH_PATH)

    conn = get_connection()

    with conn.cursor() as cur:
        for feature in FEATURES:
            ref_mean = float(reference_df[feature].mean())
            cur_mean = float(batch_df[feature].mean())
            ref_std = float(reference_df[feature].std())
            cur_std = float(batch_df[feature].std())

            mean_shift = abs(cur_mean - ref_mean)
            std_shift = abs(cur_std - ref_std)

            drift_flag = mean_shift > (0.2 * abs(ref_mean) if ref_mean != 0 else 1.0)

            cur.execute(
                """
                INSERT INTO data_drift_metrics
                (run_time, feature_name, reference_mean, current_mean, reference_std, current_std, mean_shift, std_shift, drift_flag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(),
                    feature,
                    ref_mean,
                    cur_mean,
                    ref_std,
                    cur_std,
                    mean_shift,
                    std_shift,
                    drift_flag,
                ),
            )

    conn.commit()
    conn.close()
    print("Data drift detection completed.")


if __name__ == "__main__":
    main()