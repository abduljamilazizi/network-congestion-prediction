from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Optional LSTM
try:
    from tensorflow import keras
    LSTM_AVAILABLE = True
except:
    LSTM_AVAILABLE = False

# =========================
# Load Best Model
# =========================
MODEL_PATH_RF = "models/best_model.pkl"
MODEL_PATH_LSTM = "models/best_model.h5"

model = None
model_type = None

if os.path.exists(MODEL_PATH_RF):
    model = joblib.load(MODEL_PATH_RF)
    model_type = "rf"

elif os.path.exists(MODEL_PATH_LSTM) and LSTM_AVAILABLE:
    model = keras.models.load_model(MODEL_PATH_LSTM)
    model_type = "lstm"

else:
    raise Exception("No trained model found! Run training pipeline first.")

# =========================
# FastAPI App
# =========================
app = FastAPI(title="Network Congestion Prediction API")

# =========================
# Input Schema
# =========================
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


# =========================
# Home Endpoint
# =========================
@app.get("/")
def home():
    return {
        "message": "Network Congestion Prediction API Running",
        "model_loaded": model_type
    }


# =========================
# Predict Endpoint
# =========================
@app.post("/predict")
def predict(data: NetworkInput):

    # Convert input to dataframe
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
        "Fwd Packet Length Std": data.Fwd_Packet_Length_Std,
    }

    input_df = pd.DataFrame([input_dict])

    # =========================
    # Prediction Logic
    # =========================
    if model_type == "rf":
        prediction = model.predict(input_df)[0]

    elif model_type == "lstm":
        input_array = input_df.values.astype("float32")
        input_array = input_array.reshape((1, 1, input_array.shape[1]))
        prediction = (model.predict(input_array) > 0.5).astype(int)[0][0]

    else:
        raise HTTPException(status_code=500, detail="Model type unknown")

    label = "BENIGN" if prediction == 0 else "ATTACK"

    # =========================
    # Logging
    # =========================
    os.makedirs("logs", exist_ok=True)

    log_data = input_dict.copy()
    log_data["timestamp"] = datetime.now().isoformat()
    log_data["model"] = model_type
    log_data["prediction"] = int(prediction)
    log_data["label"] = label

    log_df = pd.DataFrame([log_data])
    log_file = "logs/predictions.csv"

    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_df.to_csv(log_file, mode="w", header=True, index=False)

    return {
        "model_used": model_type,
        "prediction": int(prediction),
        "label": label
    }