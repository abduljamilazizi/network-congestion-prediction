# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements an end-to-end MLOps workflow for network congestion prediction using the CICIDS2017 dataset.

The workflow covers:
- model tracking with MLflow
- data preprocessing and model training
- Docker-based reproducibility
- FastAPI deployment for inference
- batch orchestration with Prefect
- monitoring with PostgreSQL and Adminer
- dashboards with Streamlit and Grafana
- drift detection on new data

The final system compares **Random Forest** and **LSTM** models, selects the best model for deployment, and continuously evaluates performance on new incoming data.

---

## Problem Statement
Modern networks generate large amounts of traffic data, and abnormal traffic patterns may indicate congestion, inefficiency, or malicious activity.

The objective of this project is to use machine learning and deep learning techniques to analyze network flow data and predict traffic conditions effectively.

---

## Dataset
- **Dataset:** CICIDS2017
- **Type:** Network traffic / flow-based dataset
- **Purpose:** Used for training and evaluating machine learning models on network traffic behavior

---

## Architecture Diagram
![Architecture Diagram](docs/images/system_architecture.png.png)

---

## Project Logic
The project is organized according to the following workflow:

1. **Model Tracking**
   - Run experiments for Random Forest and LSTM
   - Log runs and metrics with MLflow
   - Select the best model

2. **Training Pipeline**
   - Load and clean data
   - Train Random Forest and LSTM
   - Save trained models and scaler

3. **Dockerization and Deployment**
   - Dockerize training and inference
   - Deploy FastAPI webservice
   - Run reproducible training with Docker Compose

4. **Monitoring**
   - Prepare reference data
   - Generate new batch data
   - Calculate monitoring metrics
   - Detect data drift, prediction drift, and performance drift
   - Store results in PostgreSQL
   - Access data through Adminer
   - Visualize with Streamlit and Grafana

---

## Project Structure
```text
network-congestion-prediction/
│
├── 01_model_tracking/
│   ├── mlflow.db
│   └── run_experiments.py
│
├── 02_training_pipeline/
│   └── src/
│       ├── data/
│       │   ├── load_data.py
│       │   └── clean_data.py
│       └── models/
│           ├── train_model.py
│           ├── train_model_api.py
│           ├── train_with_mlflow.py
│           └── train_lstm.py
│
├── 03_dockerization_and_deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── batch/
│   │   ├── __init__.py
│   │   ├── deploy.py
│   │   └── train_predict_scheduled.py
│   └── webservices/
│       └── app.py
│
├── 04_monitoring/
│   ├── data/
│   │   ├── reference/
│   │   │   └── reference_data.csv
│   │   └── current_batches/
│   │       └── new_data.csv
│   ├── scripts/
│   │   ├── prepare_reference.py
│   │   ├── generate_batch.py
│   │   ├── calculate_metrics.py
│   │   ├── detect_data_drift.py
│   │   ├── detect_prediction_drift.py
│   │   ├── detect_performance_drift.py
│   │   └── monitor.py
│   └── dashboard/
│       └── app.py
│
├── batch/
├── dashboard/
├── monitoring/
├── src/
├── data/
├── models/
├── docs/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

## Models Used

### Random Forest
- A machine learning model suitable for structured tabular data
- Easy to train and deploy
- Used as the final API model for inference

### LSTM
- A deep learning model suitable for sequential learning
- Used to compare deep learning with a classical machine learning approach
- Monitored and evaluated alongside Random Forest

---

## Model Performance / Results

| Model | Accuracy | Notes |
|------|----------|------|
| Random Forest | ~99% | Strong performance on structured traffic features |
| LSTM | ~87% | Lower than Random Forest but useful for comparison |

---

## Best Model Selection
The best model is selected by comparing evaluation metrics from all trained models.

This is handled in `run_experiments.py`, where:
- Random Forest and LSTM are both trained
- their metrics are logged in MLflow
- their accuracies are compared
- the best model is written to:

```text
models/best_model_from_mlflow.txt
```

In this project, **Random Forest** was selected as the final deployed model.

---

## MLflow Usage
MLflow was used to track and compare experiments.

The following were logged:
- model type
- parameters
- metrics
- runs
- artifacts

This supports reproducibility and transparent best-model selection.

---

## Reproducibility with Docker

### Build and run the services
```cmd
docker compose up --build
```

This starts:
- FastAPI API
- PostgreSQL
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

This makes the project reproducible because another user can:
- build the Docker environment
- train the models
- run inference
- deploy FastAPI
- run monitoring

---

## FastAPI Deployment

### Run locally
```cmd
uvicorn src.deployment.app:app --reload
```

Open:
```text
http://127.0.0.1:8000/docs
```

### API Endpoints
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

---

## Batch Pipeline with Prefect
Batching is implemented in the `batch/` folder.

Main files:
- `batch/train_predict_scheduled.py`
- `batch/deploy.py`

### Start Prefect server
```cmd
project_env\Scripts\activate
prefect server start
```

### Deploy the flow
```cmd
project_env\Scripts\activate
set PREFECT_API_URL=http://127.0.0.1:4200/api
python -m batch.deploy
```

### Run the deployment manually
```cmd
project_env\Scripts\activate
set PREFECT_API_URL=http://127.0.0.1:4200/api
prefect deployment run "network_congestion_batch_predict/network-congestion-daily"
```

### Open Prefect UI
```text
http://127.0.0.1:4200
```

---

## Monitoring Pipeline

The monitoring pipeline evaluates the performance of the deployed models on new incoming data.

### Monitoring logic
The monitoring pipeline is modular and follows these steps:

1. `prepare_reference.py`
   - prepares the reference dataset from the cleaned CICIDS data

2. `generate_batch.py`
   - creates the current batch of new incoming data

3. `calculate_metrics.py`
   - evaluates Random Forest and LSTM on the new batch
   - calculates accuracy, precision, recall, and F1 score
   - writes results to PostgreSQL

4. `detect_data_drift.py`
   - compares feature distributions between reference and current batch

5. `detect_prediction_drift.py`
   - compares prediction distribution across runs

6. `detect_performance_drift.py`
   - compares current metrics with previous monitoring runs

7. `monitor.py`
   - orchestrates the full monitoring workflow

### Run monitoring
```cmd
python monitoring\monitor.py
```

---

## Database Setup

### Database
The project uses **PostgreSQL** as the monitoring database.

### Adminer
**Adminer** is attached to PostgreSQL for browser-based database access.

Open:
```text
http://127.0.0.1:8080
```

Adminer login:
- System: `PostgreSQL`
- Server: `postgres`
- Username: `postgres`
- Password: `postgres`
- Database: `monitoring_db`

### Important note
- **PostgreSQL** stores the data
- **Adminer** is used to view and query that data

---

## Database Tables

### `monitoring_metrics`
Stores summary metrics for each monitoring run:
- run time
- model name
- accuracy
- precision
- recall
- f1 score
- total samples
- benign count
- attack count

### `prediction_logs`
Stores detailed prediction records:
- run time
- model name
- prediction
- label name

### `data_drift_metrics`
Stores feature-level drift information:
- feature name
- reference mean and std
- current mean and std
- mean shift
- std shift
- drift flag

### `prediction_drift_metrics`
Stores prediction distribution changes:
- current benign/attack rate
- previous benign/attack rate
- rate shifts
- drift flag

### `performance_drift_metrics`
Stores performance degradation information:
- current accuracy
- previous accuracy
- current F1
- previous F1
- accuracy drop
- F1 drop
- drift flag

---

## Important SQL Queries

### Latest monitoring metrics
```sql
SELECT * FROM monitoring_metrics ORDER BY id DESC;
```

### Latest prediction logs
```sql
SELECT * FROM prediction_logs ORDER BY id DESC;
```

### Data drift
```sql
SELECT * FROM data_drift_metrics ORDER BY id DESC;
```

### Prediction drift
```sql
SELECT * FROM prediction_drift_metrics ORDER BY id DESC;
```

### Performance drift
```sql
SELECT * FROM performance_drift_metrics ORDER BY id DESC;
```

---

## Dashboards

### Streamlit
Run:
```cmd
streamlit run dashboard\app.py
```

Open:
```text
http://localhost:8501
```

The Streamlit dashboard shows:
- latest RF metrics
- latest LSTM metrics
- comparison between models
- prediction logs

### Grafana
Open:
```text
http://127.0.0.1:3000
```

Grafana is connected to PostgreSQL and visualizes:
- Accuracy by Model
- F1 Score by Model
- Precision by Model
- Recall by Model
- Benign vs Attack Counts
- Total Samples Processed
- Data Drift: Mean Shift by Feature
- Prediction Drift: Attack Rate Shift
- Performance Drift: Accuracy Drop

---

## Drift Detection

### Data Drift
Detects whether the incoming batch data distribution has changed compared to the reference dataset.

### Prediction Drift
Detects whether the prediction distribution has changed across monitoring runs.

### Performance Drift
Detects whether model performance has degraded compared to previous monitoring runs.

This makes the monitoring pipeline more robust and closer to real MLOps practice.

---

## Prediction Logging
Predictions are also logged in:

```text
logs/predictions.csv
```

This supports:
- monitoring
- traceability
- debugging
- auditing
- future retraining

---

## How to Demonstrate the Project

### Reproducibility
- show `Dockerfile`
- show `docker-compose.yml`
- run Docker training
- run FastAPI deployment

### Monitoring
- run `python monitoring\monitor.py`
- show Adminer tables
- show Streamlit dashboard
- show Grafana dashboard

### Batching
- show Prefect server
- show deployment
- show flow runs

### GitHub
- show the teacher-style folders:
  - `01_model_tracking`
  - `02_training_pipeline`
  - `03_dockerization_and_deployment`
  - `04_monitoring`

---

## Created by
**Abdul Jamil Azizi**

## Supervised by
**Professor Forooz Shahbazi Avarvand**
