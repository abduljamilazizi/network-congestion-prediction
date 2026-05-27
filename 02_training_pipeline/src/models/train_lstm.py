import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load dataset
data = pd.read_csv("data/processed/cleaned_network_data.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Convert label to numeric
data["Label"] = data["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# Use the same 10 features as API model
selected_features = [
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
]

# Keep only required columns
data = data[selected_features + ["Label"]]

# Sample for faster training
data = data.sample(n=50000, random_state=42)

X = data[selected_features].values
y = data["Label"].values

# Scale features
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Save scaler for later inference/monitoring use
joblib.dump(scaler, "models/lstm_scaler.pkl")

# Reshape for LSTM: (samples, timesteps, features)
X = X.reshape((X.shape[0], 1, X.shape[1]))

# One-hot encode labels
y = to_categorical(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Build LSTM model
model = Sequential([
    LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    Dense(32, activation="relu"),
    Dense(2, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train
history = model.fit(
    X_train, y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# Evaluate
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

print(classification_report(y_test_classes, y_pred_classes))

# Save model
model.save("models/lstm_model.h5")
print("LSTM model saved to models/lstm_model.h5")
print("LSTM scaler saved to models/lstm_scaler.pkl")