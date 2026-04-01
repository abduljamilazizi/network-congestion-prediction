# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements an end-to-end MLOps workflow for network congestion prediction using the CICIDS2017 dataset.

The workflow includes data loading, cleaning, model training, experiment tracking with MLflow, best model selection, deployment using FastAPI, containerization with Docker, batch scheduling with Prefect, and prediction logging for monitoring.

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
Dataset → Data Loading → Data Cleaning → Feature Selection → Model Training → MLflow Tracking → Best Model Selection → FastAPI Deployment → Docker Containerization → Prefect Scheduling → Prediction Logging

## Project Structure
```text
network-congestion-prediction/
│
├── batch/
│   ├── __init__.py
│   ├── deploy.py
│   └── train_predict_scheduled.py
│
├── docs/
│   └── images/
│       └── system_architecture.png.png
│
├── logs/
│   └── predictions.csv
│
├── models/
│   └── random_forest_model.pkl
│
├── src/
│   ├── data/
│   │   ├── load_data.py
│   │   └── clean_data.py
│   ├── deployment/
│   │   └── app.py
│   └── models/
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
## Models Used

### Random Forest
- A machine learning model suitable for structured tabular data
- Easy to train and deploy
- Performed better in this project

### LSTM
- A deep learning model suitable for sequential or time-series learning
- Used to compare deep learning with a classical machine learning approach
- Performed lower than Random Forest for this dataset

## Model Performance / Results

| Model | Accuracy | Notes |
|------|----------|------|
| Random Forest | ~99% | Strong performance on structured traffic features |
| LSTM | ~85% | Lower performance because the dataset is mainly tabular |

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

## Unified Environment Setup
This project uses a single virtual environment for both Random Forest and LSTM.

### Create and activate the environment
cmd
python -m venv project_env
project_env\Scripts\activate
pip install -r requirements.txt
