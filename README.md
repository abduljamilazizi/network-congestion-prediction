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

## Models Used
Two models were trained and compared:

- **Random Forest**
  - Suitable for structured tabular data
  - Performed better in this project

- **LSTM**
  - Suitable for sequential/time-series data
  - Used for comparison with a deep learning approach

## Model Performance
| Model | Accuracy | Notes |
|------|----------|------|
| Random Forest | ~99% | Strong performance on tabular traffic features |
| LSTM | ~85% | Lower performance because dataset is mostly tabular |

## Why Random Forest Performed Better
Random Forest achieved better results because the CICIDS2017 dataset mainly contains structured tabular network flow features. LSTM is better suited for sequential time-series data, so it was less effective here.

## Project Pipeline
Dataset → Data Loading → Data Cleaning → Feature Selection → Model Training → MLflow Tracking → Best Model Selection → FastAPI Deployment → Prediction Logging

## MLflow Usage
MLflow was used to:
- Track experiment runs
- Log model parameters
- Log evaluation metrics
- Compare Random Forest and LSTM results
- Support best model selection

## Best Model Selection
The best model is selected by comparing evaluation metrics from all trained models.  
The pipeline chooses the model with the best performance on validation/test data based on the defined comparison metric.

In this project, **Random Forest** was selected as the final model for deployment.

## API Deployment
The trained model is deployed using **FastAPI**.

### Endpoint
`POST /predict`

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
