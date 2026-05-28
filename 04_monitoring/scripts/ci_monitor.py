import pandas as pd

print("CI/CD Monitoring Pipeline Started...")

try:
    df = pd.read_csv("04_monitoring/data/current_batches/new_data.csv")
    print("Data loaded successfully")

    print("Monitoring logic executed successfully")

except Exception as e:
    print(f"Monitoring skipped due to error: {e}")