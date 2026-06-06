# 🚀 Network Congestion Prediction — End-to-End MLOps Pipeline

**Abdul Jamil Azizi** · Master in IT Digitalization and Sustainability  
Lucerne University of Applied Sciences and Arts (HSLU) · Module: Artificial Intelligence

[![CI/CD](https://github.com/abduljamilazizi/network-congestion-prediction/actions/workflows/ci-cd-pipeline.yml/badge.svg)](https://github.com/abduljamilazizi/network-congestion-prediction/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-25.0.3-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📌 Project Overview

This project implements a **complete, production-grade MLOps pipeline** for predicting network congestion from flow-level traffic data. The contribution is architectural: it demonstrates how operational practices identified in the MLOps literature can be realised in a reproducible, fully automated system using only open-source tools.

Two model families are compared:

| Model | Accuracy | Precision | Recall | F1 | Selected |
|---|---|---|---|---|---|
| **Random Forest** | **0.9939** | **>0.99** | **>0.99** | **>0.99** | ✅ |
| LSTM | 0.8528 | — | — | — | ❌ |

The Random Forest is selected as the production model due to its superior performance on the tabular, non-sequential nature of flow-level network statistics.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OFFLINE PIPELINE                         │
│  CICIDS2017 Data → Preprocessing → RF + LSTM Training →         │
│  MLflow Tracking → Model Selection → Artefact + Schema Export   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ model binary + feature schema
┌───────────────────────────▼─────────────────────────────────────┐
│                        ONLINE STACK                             │
│                                                                 │
│  FastAPI /predict ←── Prefect Batch Pipeline ←── New Data       │
│       │                                                         │
│       ▼                                                         │
│  PostgreSQL (5 tables) ──► Grafana Dashboards                   │
│       │                                                         │
│       ▼                                                         │
│  Drift Detection (data drift · prediction drift · perf drift)   │
│                                                                 │
│  GitHub Actions CI/CD (35 consecutive ✅ runs, <60s each)       │
└─────────────────────────────────────────────────────────────────┘
```

The training and serving stages share a single **artefact contract** — a serialised model binary accompanied by a persisted feature schema — which decouples the model's identity from its training environment and prevents train/serve feature skew.

---

## ⚙️ Tool Stack

| Tool | Version | Role |
|---|---|---|
| FastAPI | 0.110.0 | REST prediction API (`/predict`, `/predict/batch`) |
| Docker | 25.0.3 | Containerisation and environment isolation |
| Prefect | 2.16.5 | Batch workflow scheduling and orchestration |
| PostgreSQL | 16.2 | Relational metric and prediction log store |
| Grafana | 10.4.1 | Multi-panel telemetry visualisation |
| MLflow | latest | Experiment tracking and model registry |
| Pytest | 8.0.2 | Test runner and coverage gate (≥60% required) |
| GitHub Actions | v4 | CI/CD pipeline automation |

All versions are pinned in `requirements.txt` and the Dockerfile for reproducible builds.

---

## 📂 Repository Structure

```
network-congestion-prediction/
│
├── .github/
│   └── workflows/              # GitHub Actions CI/CD pipeline YAML
│
├── 01_model_tracking/          # MLflow experiment tracking
│
├── 02_training_pipeline/
│   └── src/                    # Training scripts: RF + LSTM, preprocessing, schema export
│
├── 03_dockerization_and_deployment/
│   ├── main.py                 # FastAPI application
│   ├── Dockerfile              # python:3.11-slim container definition
│   └── docker-compose.yml      # Multi-service orchestration
│
├── 04_monitoring/
│   ├── scripts/
│   │   ├── monitor.py          # Classification metrics → PostgreSQL
│   │   ├── data_drift.py       # KS-test / Jensen-Shannon drift detection
│   │   ├── prediction_drift.py # Attack-rate shift monitoring
│   │   └── performance_drift.py
│   └── dashboard/
│       └── app.py              # Streamlit dashboard
│
├── 05_streaming/               # Row-by-row real-time inference pipeline
│
├── docs/                       # Project report (IEEE format)
│
└── README.md
```

---

## 🗄️ Database Schema

Five PostgreSQL tables back the monitoring stack:

| Table | Purpose |
|---|---|
| `monitoring_metrics` | Timestamped accuracy / precision / recall / F1 per evaluation cycle |
| `prediction_logs` | Individual flow-level predictions from batch pipeline |
| `data_drift_metrics` | Feature-level mean shift vs. training reference distribution |
| `prediction_drift_metrics` | Attack-rate shift over time |
| `performance_drift_metrics` | Longitudinal performance degradation signals |

---

## ▶️ How to Run

### Prerequisites
- Python 3.11
- Docker Desktop
- PostgreSQL 16
- Grafana

### 1. Clone and activate environment

```bash
git clone https://github.com/abduljamilazizi/network-congestion-prediction.git
cd network-congestion-prediction
python -m venv project_env
# Windows:
project_env\Scripts\activate
# macOS/Linux:
source project_env/bin/activate
pip install -r requirements.txt
```

### 2. Train the models

```bash
cd 02_training_pipeline/src
python train.py
```

This trains both Random Forest and LSTM, logs experiments to MLflow, selects the best model by F1-score, and serialises the model binary + feature schema.

### 3. Start the API

```bash
cd 03_dockerization_and_deployment
uvicorn main:app --reload
# API available at http://127.0.0.1:8000
# Interactive docs at http://127.0.0.1:8000/docs
```

### 4. Run with Docker (recommended)

```bash
cd 03_dockerization_and_deployment
docker compose up --build
```

> **Note on network namespaces:** Inside the Docker network, services address each other by service name (e.g. `http://api:8000`). On the host machine, use `http://localhost:8000`. Misconfiguring this is the most common first-run error — check your `.env` file if connections fail.

### 5. Run the monitoring script

```bash
python 04_monitoring/scripts/monitor.py
```

Metrics are written to PostgreSQL and immediately queryable by Grafana.

### 6. Start the Prefect batch pipeline

```bash
prefect server start
# In a separate terminal:
python 04_monitoring/scripts/prefect_flow.py
```

### 7. Launch the Streamlit dashboard

```bash
streamlit run 04_monitoring/dashboard/app.py
```

---

## 🧪 Testing

```bash
pytest --cov=. --cov-report=term-missing
```

The test suite has three layers:
- **Schema Validation Tests** — Pydantic field constraint checks at the API boundary
- **Endpoint Integrity Tests** — FastAPI test client asserting correct JSON structure and status codes
- **Orchestration Flow Tests** — Prefect task block preprocessing and column-layout validation

A **minimum 60% line coverage gate** is enforced in CI. Any commit falling below this threshold blocks the pull request.

---

## 🔁 CI/CD Pipeline

The GitHub Actions pipeline runs on every push to `main` and completes in under 60 seconds. It executes 22 steps:

```
Set up job → Install dependencies → Code quality check (linting) →
Create dummy data → Wait for PostgreSQL → Run monitoring validation →
Run Pytest suite → Model performance check → Build Docker image →
Tag Docker image → Deploy application → CD status report → Cleanup
```

**35 consecutive successful runs** on the main branch with zero failures.

[View Actions →](https://github.com/abduljamilazizi/network-congestion-prediction/actions)

---

## 📊 Monitoring & Drift Detection

The monitoring subsystem tracks three drift types continuously:

- **Data drift** — Kolmogorov-Smirnov test on input feature distributions vs. training reference snapshot. `Flow_Duration` was identified as the primary source of distributional movement.
- **Prediction drift** — Attack-rate shift over time via Population Stability Index (PSI). Peaked at ~0.19 on 05 May 2026; consistent with transient traffic bursts, not sustained concept drift.
- **Performance drift** — All four classification metrics (accuracy, precision, recall, F1) held at **1.0** across the full monitored observation window (2026-05-27 to 2026-06-05).

---

## ⚠️ Known Limitations

- **Static reference window:** The drift baseline is a fixed snapshot from training time. Long-term infrastructure changes will produce false-positive alerts until the reference is manually refreshed.
- **Single-host orchestration:** Prefect runs on a single-host agent; horizontal scaling requires migration to a distributed execution environment.
- **Tabular-only ingestion:** Raw PCAP streams cannot be ingested without first computing flow-level aggregates.

---

## 🔮 Future Work

- Automated retraining triggered by PostgreSQL drift threshold breaches
- Adaptive sliding-window reference distributions to reduce false-positive drift alerts
- Edge inference on network switches/gateways for reduced serving latency

---

## 📄 Report

The full IEEE-format project report is available in [`docs/`](./docs/).

---

## 🤖 AI Tool Usage

Claude, Chatgpt, Google gemini as well as Grammerly was used in an assistive capacity for LaTeX formatting, academic writing refinement, and code review support. All technical decisions architecture, tool selection, model choice, evaluation methodology were made exclusively by the author. See Section XVIII of the project report for full disclosure.

---

## 👨‍💻 Author

**Abdul Jamil Azizi**  
Master in IT Digitalization and Sustainability  
Lucerne University of Applied Sciences and Arts  
📧 abduljamil.azizi@stud.hslu.ch  
🔗 [github.com/abduljamilazizi](https://github.com/abduljamilazizi)

---

*Supervised by Professor Dr. Forooz Shahbaz Avarvand*
