import pandas as pd
import numpy as np
import os

DATA_PATH = "data/raw"

files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

dataframes = []

for file in files:
    print("Loading:", file)
    df = pd.read_csv(os.path.join(DATA_PATH, file), low_memory=False)
    dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

print("Original Shape:", data.shape)

# Replace infinite values
data.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove rows with missing values
data.dropna(inplace=True)

print("Cleaned Shape:", data.shape)

# Save cleaned dataset
data.to_csv("data/processed/cleaned_network_data.csv", index=False)

print("Cleaned dataset saved.") 
