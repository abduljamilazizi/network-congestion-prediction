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


def get_current_metrics(cur, model_name):
    cur.execute(
        """
        SELECT accuracy, f1_score
        FROM monitoring_metrics
        WHERE model_name = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (model_name,),
    )
    return cur.fetchone()


def get_previous_metrics(cur, model_name):
    cur.execute(
        """
        SELECT accuracy, f1_score
        FROM monitoring_metrics
        WHERE model_name = %s
        ORDER BY id DESC
        OFFSET 1 LIMIT 1
        """,
        (model_name,),
    )
    return cur.fetchone()


def main():
    conn = get_connection()

    with conn.cursor() as cur:
        for model_name in ["rf", "lstm"]:
            current = get_current_metrics(cur, model_name)
            if not current:
                continue

            current_accuracy, current_f1 = current
            previous = get_previous_metrics(cur, model_name)

            previous_accuracy = None
            previous_f1 = None
            accuracy_drop = None
            f1_drop = None
            drift_flag = False

            if previous:
                previous_accuracy, previous_f1 = previous
                accuracy_drop = previous_accuracy - current_accuracy
                f1_drop = previous_f1 - current_f1
                drift_flag = (accuracy_drop > 0.1) or (f1_drop > 0.1)

            cur.execute(
                """
                INSERT INTO performance_drift_metrics
                (run_time, model_name, current_accuracy, previous_accuracy, current_f1, previous_f1,
                 accuracy_drop, f1_drop, drift_flag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(),
                    model_name,
                    current_accuracy,
                    previous_accuracy,
                    current_f1,
                    previous_f1,
                    accuracy_drop,
                    f1_drop,
                    drift_flag,
                ),
            )

    conn.commit()
    conn.close()
    print("Performance drift detection completed.")


if __name__ == "__main__":
    main()