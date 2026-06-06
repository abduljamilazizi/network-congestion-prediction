# 🚀 Network Congestion Prediction (MLOps Project)

This project implements a complete MLOps pipeline for predicting network congestion using Machine Learning and Deep Learning models, along with monitoring, orchestration, and CI/CD automation.

## 📌 Project Overview

- Random Forest (ML)
- LSTM (Deep Learning)
- Monitoring & Metrics
- Prefect (Batch)
- Streaming Simulation
- Grafana / Streamlit Visualization
- CI/CD (GitHub Actions)
- Docker (Deployment-ready)

## 🏗️ Architecture

Data → Training → Models → Monitoring → Visualization → CI/CD → Deployment

## ⚙️ Technologies

Python, Scikit-learn, TensorFlow, MLflow, Prefect, PostgreSQL, Grafana, Streamlit, Docker, GitHub Actions

## 📊 Monitoring

- Accuracy
- Precision
- Recall
- F1 Score
- Stored in PostgreSQL

## 🔁 CI/CD

- Runs on git push
- Validates system
- Builds Docker image
- Simulates deployment

## ▶️ Run

Activate:
project_env\Scripts\activate

API:
uvicorn main:app --reload

Monitoring:
python 04_monitoring/scripts/monitor.py

Streaming:
python streaming/streaming_pipeline.py

Prefect:
prefect server start

Dashboard:
streamlit run 04_monitoring/dashboard/app.py

## 👨‍💻 Author

Abdul Jamil Azizi
https://github.com/abduljamilazizi
