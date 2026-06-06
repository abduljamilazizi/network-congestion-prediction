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
