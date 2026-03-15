# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements a machine learning system to detect abnormal network traffic and potential congestion.

The system trains a Random Forest model using the CICIDS2017 dataset and deploys the model using FastAPI.

## System Architecture

```mermaid
flowchart TD

A[CICIDS2017 Dataset] --> B[Data Cleaning & Feature Selection]

B --> C1[Random Forest Training]
B --> C2[LSTM Training]

C1 --> D1[Random Forest Model]
C2 --> D2[LSTM Model]

D1 --> E[MLflow Experiment Tracking]
D2 --> E

E --> F[FastAPI Prediction API]

F --> G[User Request /predict]

G --> H[Model Prediction]

H --> I[Prediction Monitoring Logs]

I --> J[logs/predictions.csv]

---

## Technologies Used

- Python
- Scikit-learn
- FastAPI
- MLflow
- Pandas
- Git & GitHub

---

## Project Pipeline

Dataset → Data Cleaning → Model Training → MLflow Tracking → API Deployment → Monitoring

---

## Model Deployment

The trained model is deployed using FastAPI.

Run the API:
