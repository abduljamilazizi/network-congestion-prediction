from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from datetime import datetime

# Load trained model
model = joblib.load("models/random_forest_model.pkl")

app = FastAPI(title="Network Congestion Prediction API")

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Define input schema
class NetworkInput(BaseModel):
    Destination_Port: float
    Flow_Duration: float
    Total_Fwd_Packets: float
    Total_Backward_Packets: float
    Total_Length_of_Fwd_Packets: float
    Total_Length_of_Bwd_Packets: float
    Fwd_Packet_Length_Max: float
    Fwd_Packet_Length_Min: float
    Fwd_Packet_Length_Mean: float
    Fwd_Packet_Length_Std: float

@app.get("/")
def home():
    return {"message": "Network Congestion Prediction API is running"}

@app.post("/predict")
def predict(data: NetworkInput):
    input_dict = {
        "Destination Port": data.Destination_Port,
        "Flow Duration": data.Flow_Duration,
        "Total Fwd Packets": data.Total_Fwd_Packets,
        "Total Backward Packets": data.Total_Backward_Packets,
        "Total Length of Fwd Packets": data.Total_Length_of_Fwd_Packets,
        "Total Length of Bwd Packets": data.Total_Length_of_Bwd_Packets,
        "Fwd Packet Length Max": data.Fwd_Packet_Length_Max,
        "Fwd Packet Length Min": data.Fwd_Packet_Length_Min,
        "Fwd Packet Length Mean": data.Fwd_Packet_Length_Mean,
        "Fwd Packet Length Std": data.Fwd_Packet_Length_Std
    }

    input_df = pd.DataFrame([input_dict])
    prediction = int(model.predict(input_df)[0])
    label = "BENIGN" if prediction == 0 else "ATTACK"

    # Log prediction to CSV
    log_entry = input_dict.copy()
    log_entry["timestamp"] = datetime.now().isoformat()
    log_entry["prediction"] = prediction
    log_entry["label"] = label

    log_df = pd.DataFrame([log_entry])
    log_file = "logs/predictions.csv"

    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_df.to_csv(log_file, mode="w", header=True, index=False)

    return {
        "prediction": prediction,
        "label": label
    }