from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Literal
import joblib
import pandas as pd
import os
from datetime import datetime
import numpy as np

# Optional LSTM support
LSTM_AVAILABLE = True
LSTM_LOAD_ERROR = None
try:
    from tensorflow import keras
except Exception as e:
    LSTM_AVAILABLE = False
    LSTM_LOAD_ERROR = f"TensorFlow import failed: {e}"

# Load Random Forest model
rf_model = joblib.load("models/random_forest_model.pkl")

# Load LSTM model if available
lstm_model = None
if LSTM_AVAILABLE:
    try:
        lstm_model = keras.models.load_model("models/lstm_model.h5")
    except Exception as e:
        LSTM_AVAILABLE = False
        LSTM_LOAD_ERROR = f"LSTM model load failed: {e}"

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


def build_input_dict(data: NetworkInput) -> dict:
    return {
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


@app.get("/")
def home():
    return {"message": "Network Congestion Prediction API is running"}


@app.get("/models")
def list_models():
    return {
        "available_models": {
            "rf": True,
            "lstm": LSTM_AVAILABLE,
        },
        "lstm_status": "loaded" if LSTM_AVAILABLE else LSTM_LOAD_ERROR,
    }


@app.post("/predict")
def predict(
    data: NetworkInput,
    model: Literal["rf", "lstm"] = Query(
        default="rf",
        description="Choose prediction model: 'rf' for Random Forest or 'lstm' for LSTM"
    ),
):
    input_dict = build_input_dict(data)
    input_df = pd.DataFrame([input_dict])

    if model == "rf":
        prediction = int(rf_model.predict(input_df)[0])

    elif model == "lstm":
        if not LSTM_AVAILABLE or lstm_model is None:
            raise HTTPException(
                status_code=500,
                detail=f"LSTM model is not available. {LSTM_LOAD_ERROR}"
            )

        # LSTM was trained on 10 features reshaped to (samples, 1, features)
        input_array = input_df.values.astype("float32")
        input_array = input_array.reshape((input_array.shape[0], 1, input_array.shape[1]))

        lstm_probs = lstm_model.predict(input_array, verbose=0)
        prediction = int(np.argmax(lstm_probs, axis=1)[0])

    else:
        raise HTTPException(status_code=400, detail="Unsupported model")

    label = "BENIGN" if prediction == 0 else "ATTACK"

    # Log prediction to CSV
    log_entry = input_dict.copy()
    log_entry["timestamp"] = datetime.now().isoformat()
    log_entry["model"] = model
    log_entry["prediction"] = prediction
    log_entry["label"] = label

    log_df = pd.DataFrame([log_entry])
    log_file = "logs/predictions.csv"

    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_df.to_csv(log_file, mode="w", header=True, index=False)

    return {
        "model": model,
        "prediction": prediction,
        "label": label,
    }