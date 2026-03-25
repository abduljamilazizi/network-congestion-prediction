# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements an end-to-end MLOps workflow for network congestion prediction using the CICIDS2017 dataset.

The workflow includes data loading, cleaning, model training, experiment tracking with MLflow, best model selection, deployment using FastAPI, and prediction logging for monitoring.

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
Dataset → Data Loading → Data Cleaning → Feature Selection → Model Training → MLflow Tracking → Best Model Selection → FastAPI Deployment → Prediction Logging

## Project Structure
```text
network-congestion-prediction/
│
├── data/
│   ├── raw/
│   └── processed/
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
│   └── deployment/
│       └── app.py
│
├── README.md
├── requirements.txt
└── main.py

### 8. Models Used
```markdown
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
## Model Performance / Results
| Model | Accuracy | Notes |
|------|----------|------|
| Random Forest | ~99% | Strong performance on structured traffic features |
| LSTM | ~85% | Lower performance because the dataset is mainly tabular |
