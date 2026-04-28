import pandas as pd
import os

DATA_PATH = "data/raw"

files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

dataframes = []

for file in files:
    print("Loading:", file)
    file_path = os.path.join(DATA_PATH, file)
    df = pd.read_csv(file_path, low_memory=False)
    dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

print("\nDataset loaded successfully")
print("Shape:", data.shape)

print("\nColumns:")
print(data.columns)

print("\nFirst rows:")
print(data.head())