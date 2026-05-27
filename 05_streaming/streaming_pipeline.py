import time
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

DATA_PATH = "../04_monitoring/data/current_batches/new_data.csv"

def stream_data():
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print("Starting streaming simulation (Switzerland Time)...\n")

    for i, row in df.iterrows():
        current_time = datetime.now(ZoneInfo("Europe/Zurich"))

        print(f"[{current_time}] Sending data row {i+1}")
        print(row.to_dict())
        print("-" * 50)

        time.sleep(1)

    print("\nStreaming completed.")

if __name__ == "__main__":
    stream_data()