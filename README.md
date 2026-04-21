# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements an end-to-end MLOps workflow for network congestion prediction using the CICIDS2017 dataset.

The workflow includes data loading, cleaning, model training, experiment tracking with MLflow, best model selection, deployment using FastAPI, containerization with Docker, batch scheduling with Prefect, and a monitoring pipeline with PostgreSQL, Adminer, Streamlit, and Grafana.

The goal is to build a reproducible and deployment-ready machine learning pipeline for analyzing network traffic behavior.

## Problem Statement
Modern networks generate large amounts of traffic data, and abnormal traffic patterns may indicate congestion, inefficiency, or malicious activity.

The objective of this project is to use machine learning and deep learning techniques to analyze network flow data and predict traffic conditions effectively.

## Dataset
- **Dataset:** CICIDS2017
- **Type:** Network traffic / flow-based dataset
- **Why used:** It contains realistic network flow features suitable for training and evaluating machine learning models for traffic analysis.

## Architecture Diagram
![Architecture Diagram](docs/images/system_architecture.png.png)

## Project Pipeline
Dataset → Data Loading → Data Cleaning → Feature Selection → Model Training → MLflow Tracking → Best Model Selection → FastAPI Deployment → Docker Containerization → Monitoring with PostgreSQL/Adminer → Dashboard Visualization → Prediction Logging

## Project Structure
```text
network-congestion-prediction/
│
├── batch/
│   ├── __init__.py
│   ├── deploy.py
│   └── train_predict_scheduled.py
│
├── dashboard/
│   └── app.py
│
├── monitoring/
│   └── monitor.py
│
├── docs/
│   └── images/
│       └── system_architecture.png.png
│
├── data/
│   ├── processed/
│   │   └── cleaned_network_data.csv
│   └── new/
│       └── new_data.csv
│
├── logs/
│   └── predictions.csv
│
├── models/
│   ├── random_forest_model.pkl
│   ├── lstm_model.h5
│   └── lstm_scaler.pkl
│
├── src/
│   ├── data/
│   │   ├── load_data.py
│   │   └── clean_data.py
│   ├── deployment/
│   │   └── app.py
│   └── models/
│       ├── train_model.py
│       ├── train_model_api.py
│       ├── train_with_mlflow.py
│       └── train_lstm.py
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── mlflow.db
├── README.md
└── requirements.txt
```

## Models Used

### Random Forest
- A machine learning model suitable for structured tabular data
- Easy to train and deploy
- Used as the final API model for inference

### LSTM
- A deep learning model suitable for sequential learning
- Used to compare deep learning with a classical machine learning approach
- Monitored and evaluated alongside Random Forest

## Model Performance / Results

| Model | Accuracy | Notes |
|------|----------|------|
| Random Forest | ~99% | Strong performance on structured traffic features |
| LSTM | ~87% | Lower than Random Forest but still useful for comparison |

## Best Model Selection
The best model is selected by comparing evaluation metrics from all trained models.

The pipeline compares candidate models after training, logs their metrics to MLflow, and selects the model with the strongest performance.

In this project, **Random Forest** was selected as the final deployed model.

## MLflow Usage
MLflow was used to track and compare experiments.

The following were logged:
- Model name
- Parameters
- Metrics
- Runs
- Artifacts

MLflow improves reproducibility and supports transparent best model selection.

## Reproducibility with Docker

### Build and run the services
```cmd
docker compose up --build
```

This starts:
- FastAPI API
- PostgreSQL database
- Adminer
- Grafana

### Train Random Forest in Docker
```cmd
docker compose run --rm trainer_rf
```

### Train LSTM in Docker
```cmd
docker compose run --rm trainer_lstm
```

## Run FastAPI Locally
```cmd
uvicorn src.deployment.app:app --reload
```

Open:
`http://127.0.0.1:8000/docs`

## API Deployment

### Endpoints
- `GET /`
- `GET /models`
- `POST /predict`

### Example Input
```json
{
  "Destination_Port": 443,
  "Flow_Duration": 120,
  "Total_Fwd_Packets": 10,
  "Total_Backward_Packets": 8,
  "Total_Length_of_Fwd_Packets": 1200,
  "Total_Length_of_Bwd_Packets": 900,
  "Fwd_Packet_Length_Max": 300,
  "Fwd_Packet_Length_Min": 50,
  "Fwd_Packet_Length_Mean": 120,
  "Fwd_Packet_Length_Std": 30
}
```

### Example Response
```json
{
  "model": "rf",
  "prediction": 0,
  "label": "BENIGN"
}
```

## Monitoring Pipeline
The monitoring pipeline evaluates model performance on new incoming data and stores the results in PostgreSQL.

### Monitoring stack
- **PostgreSQL** stores monitoring metrics and prediction logs
- **Adminer** provides browser-based database access
- **Streamlit** provides a custom project dashboard
- **Grafana** provides professional monitoring visualizations

### Run monitoring locally
```cmd
python monitoring\monitor.py
```

### Open Adminer
`http://127.0.0.1:8080`

Adminer login:
- System: `PostgreSQL`
- Server: `postgres`
- Username: `postgres`
- Password: `postgres`
- Database: `monitoring_db`

### Open Streamlit dashboard
```cmd
streamlit run dashboard\app.py
```

Open:
`http://localhost:8501`

### Open Grafana
`http://127.0.0.1:3000`

Grafana login:
- Username: `admin`
- Password: your configured Grafana password

## Database Tables

### monitoring_metrics
Stores:
- run time
- model name
- accuracy
- precision
- recall
- f1 score
- total samples
- benign count
- attack count

### prediction_logs
Stores:
- run time
- model name
- prediction
- label name

## Example SQL Queries

### Latest monitoring metrics
```sql
SELECT * FROM monitoring_metrics ORDER BY id DESC;
```

### Latest prediction logs
```sql
SELECT * FROM prediction_logs ORDER BY id DESC;
```

### Accuracy by model
```sql
SELECT
  run_time AS time,
  accuracy,
  model_name
FROM monitoring_metrics
ORDER BY run_time;
```

## Prefect Batch Scheduling
Prefect is used to schedule and monitor batch prediction runs.

### Start Prefect server
Terminal 1:
```cmd
project_env\Scripts\activate
prefect server start
```

### Deploy the flow
Terminal 2:
```cmd
project_env\Scripts\activate
set PREFECT_API_URL=http://127.0.0.1:4200/api
python -m batch.deploy
```

### Trigger a manual run
```cmd
prefect deployment run "network_congestion_batch_predict/network-congestion-daily"
```

### Open Prefect UI
`http://127.0.0.1:4200`

## Prediction Logging
Predictions are logged in:
`logs/predictions.csv`

This supports:
- Monitoring deployed predictions
- Traceability
- Debugging
- Auditing outputs
- Supporting future retraining

## Created by
**Abdul Jamil Azizi**

## Supervised by
**Professor Forooz Shahbazi Avarvand**
