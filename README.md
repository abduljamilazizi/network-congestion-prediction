# 🚀 Network Congestion Prediction using MLOps

This project implements a complete **MLOps pipeline** for predicting network congestion using machine learning models. It covers the full lifecycle including training, deployment, monitoring, streaming, and CI/CD automation.

---

# 📌 Project Overview

The goal of this project is to:

- Predict network congestion using ML models
- Automate training and deployment
- Monitor model performance
- Detect data and prediction drift
- Simulate real-time data streaming
- Implement CI/CD for automation

---

# 🏗️ Project Structure

01_model_tracking/
02_training_pipeline/
03_dockerization_and_deployment/
04_monitoring/
05_streaming/
.github/
README.md

---

# ⚙️ Stage 1: Model Tracking (MLflow)

- Random Forest and LSTM models
- Experiment tracking with MLflow
- Model comparison

---

# 🤖 Stage 2: Training Pipeline

- Data preprocessing
- Model training and evaluation

---

# 🐳 Stage 3: Deployment (Docker + FastAPI)

- FastAPI for serving predictions
- Docker for containerization

Run API:
uvicorn src.deployment.app:app --reload

---

# 📊 Stage 4: Monitoring & Drift Detection

- Accuracy, Precision, Recall, F1-score
- Data, Prediction, and Performance Drift
- PostgreSQL for storing metrics
- Grafana for visualization

Run monitoring:
python 04_monitoring/scripts/monitor.py

---

# 🔄 Stage 5: Streaming Pipeline

- Simulates real-time data streaming

Run:
python 05_streaming/streaming_pipeline.py

---

# 🔁 Stage 6: CI/CD Pipeline

- Implemented using GitHub Actions
- Runs automatically on push
- Validates pipeline execution

---

# 🧠 System Architecture

Data → Model → Prediction → Monitoring → Database → Grafana  
                         ↓  
                     CI/CD Automation

---

# 📊 Technologies

Python, Scikit-learn, TensorFlow, MLflow, FastAPI, Docker, PostgreSQL, Grafana, GitHub Actions

---

# ▶️ Run Project

docker-compose up  
python 04_monitoring/scripts/monitor.py  
python 05_streaming/streaming_pipeline.py  
uvicorn src.deployment.app:app --reload  

---

# 🎤 Summary

Complete MLOps pipeline with training, deployment, monitoring, streaming, and CI/CD.

---

# 👨‍💻 Author

Abdul Jamil Azizi
