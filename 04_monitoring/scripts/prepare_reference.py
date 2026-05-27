import os
import pandas as pd

SOURCE_DATA = "data/processed/cleaned_network_data.csv"
OUTPUT_REFERENCE = "data/reference/reference_data.csv"

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
    os.makedirs("data/reference", exist_ok=True)

    df = pd.read_csv(SOURCE_DATA, low_memory=False)
    df.columns = df.columns.str.strip()

    df = df[SELECTED_FEATURES].copy()
    df.dropna(inplace=True)

    reference_df = df.sample(n=min(1000, len(df)), random_state=42)
    reference_df.to_csv(OUTPUT_REFERENCE, index=False)

    print(f"Reference dataset saved to {OUTPUT_REFERENCE}")
    print(f"Reference rows: {len(reference_df)}")


if __name__ == "__main__":
    main()