import os
from datetime import datetime

import psycopg2

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoring_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def get_current_rates(cur, model_name):
    cur.execute(
        """
        SELECT total_samples, benign_count, attack_count
        FROM monitoring_metrics
        WHERE model_name = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (model_name,),
    )
    row = cur.fetchone()
    if not row:
        return None

    total_samples, benign_count, attack_count = row
    return benign_count / total_samples, attack_count / total_samples


def get_previous_rates(cur, model_name):
    cur.execute(
        """
        SELECT total_samples, benign_count, attack_count
        FROM monitoring_metrics
        WHERE model_name = %s
        ORDER BY id DESC
        OFFSET 1 LIMIT 1
        """,
        (model_name,),
    )
    row = cur.fetchone()
    if not row:
        return None, None

    total_samples, benign_count, attack_count = row
    return benign_count / total_samples, attack_count / total_samples


def main():
    conn = get_connection()

    with conn.cursor() as cur:
        for model_name in ["rf", "lstm"]:
            current = get_current_rates(cur, model_name)
            if current is None:
                continue

            current_benign_rate, current_attack_rate = current
            previous_benign_rate, previous_attack_rate = get_previous_rates(cur, model_name)

            benign_shift = None
            attack_shift = None
            drift_flag = False

            if previous_benign_rate is not None and previous_attack_rate is not None:
                benign_shift = abs(current_benign_rate - previous_benign_rate)
                attack_shift = abs(current_attack_rate - previous_attack_rate)
                drift_flag = benign_shift > 0.2 or attack_shift > 0.2

            cur.execute(
                """
                INSERT INTO prediction_drift_metrics
                (run_time, model_name, current_benign_rate, current_attack_rate,
                 previous_benign_rate, previous_attack_rate, benign_rate_shift, attack_rate_shift, drift_flag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(),
                    model_name,
                    current_benign_rate,
                    current_attack_rate,
                    previous_benign_rate,
                    previous_attack_rate,
                    benign_shift,
                    attack_shift,
                    drift_flag,
                ),
            )

    conn.commit()
    conn.close()
    print("Prediction drift detection completed.")


if __name__ == "__main__":
    main()