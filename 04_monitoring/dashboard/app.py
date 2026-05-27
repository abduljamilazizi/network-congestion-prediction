import os
import pandas as pd
import psycopg2
import streamlit as st

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoring_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def load_monitoring_metrics():
    conn = get_connection()
    query = "SELECT * FROM monitoring_metrics ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def load_prediction_logs():
    conn = get_connection()
    query = "SELECT * FROM prediction_logs ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


st.set_page_config(page_title="Model Monitoring Dashboard", layout="wide")
st.title("Network Congestion Monitoring Dashboard")

metrics_df = load_monitoring_metrics()
logs_df = load_prediction_logs()

st.subheader("Latest Monitoring Metrics")
st.dataframe(metrics_df, use_container_width=True)

if not metrics_df.empty:
    st.subheader("Latest Metrics by Model")

    rf_df = metrics_df[metrics_df["model_name"] == "rf"]
    lstm_df = metrics_df[metrics_df["model_name"] == "lstm"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Random Forest")
        if not rf_df.empty:
            latest_rf = rf_df.iloc[0]
            st.metric("Accuracy", latest_rf["accuracy"])
            st.metric("Precision", latest_rf["precision_score"])
            st.metric("Recall", latest_rf["recall_score"])
            st.metric("F1 Score", latest_rf["f1_score"])
            st.metric("Benign Count", latest_rf["benign_count"])
            st.metric("Attack Count", latest_rf["attack_count"])
        else:
            st.info("No RF metrics found.")

    with col2:
        st.markdown("### LSTM")
        if not lstm_df.empty:
            latest_lstm = lstm_df.iloc[0]
            st.metric("Accuracy", latest_lstm["accuracy"])
            st.metric("Precision", latest_lstm["precision_score"])
            st.metric("Recall", latest_lstm["recall_score"])
            st.metric("F1 Score", latest_lstm["f1_score"])
            st.metric("Benign Count", latest_lstm["benign_count"])
            st.metric("Attack Count", latest_lstm["attack_count"])
        else:
            st.info("No LSTM metrics found.")

    st.subheader("Accuracy by Model")
    chart_df = metrics_df[["model_name", "accuracy"]].copy()
    st.bar_chart(chart_df.set_index("model_name"))

    st.subheader("Prediction Counts")
    count_df = metrics_df[["model_name", "benign_count", "attack_count"]].copy()
    st.bar_chart(count_df.set_index("model_name"))

st.subheader("Prediction Logs")
st.dataframe(logs_df, use_container_width=True)