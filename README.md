# Network Congestion Prediction using Machine Learning

## Project Overview
This project implements an end-to-end MLOps workflow for network congestion prediction using the CICIDS2017 dataset.

The project includes:
- Data loading and cleaning
- Model training with Random Forest and LSTM
- Experiment tracking with MLflow
- Model deployment using FastAPI
- Prediction logging for monitoring
- Version control with GitHub

## Problem Statement
The goal of this project is to predict abnormal network traffic patterns that may indicate congestion or attacks using machine learning and deep learning techniques.

## Dataset
- **Dataset:** CICIDS2017
- **Type:** Network traffic / flow-based dataset
- **Use in project:** Used for training and evaluating models for network congestion prediction

## Architecture
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
