import os
import pandas as pd

SOURCE_DATA = "data/processed/cleaned_network_data.csv"
OUTPUT_BATCH = "data/new/new_data.csv"

SELECTED_FEATURES = [
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
    "Label",
]


def main():
    os.makedirs("data/new", exist_ok=True)

    df = pd.read_csv(SOURCE_DATA, low_memory=False)
    df.columns = df.columns.str.strip()

    df = df[SELECTED_FEATURES].copy()
    df.dropna(inplace=True)

    benign = df[df["Label"] == "BENIGN"].sample(n=min(50, len(df[df["Label"] == "BENIGN"])), random_state=42)
    attack = df[df["Label"] != "BENIGN"].sample(n=min(50, len(df[df["Label"] != "BENIGN"])), random_state=42)

    batch_df = pd.concat([benign, attack], ignore_index=True)
    batch_df["Label"] = batch_df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

    batch_df.to_csv(OUTPUT_BATCH, index=False)

    print(f"New monitoring batch saved to {OUTPUT_BATCH}")
    print(f"Batch rows: {len(batch_df)}")


if __name__ == "__main__":
    main()