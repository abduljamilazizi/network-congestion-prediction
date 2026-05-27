# Streaming Pipeline (Real-Time Simulation)

## Overview
This module simulates a real-time data streaming pipeline for network congestion prediction.

It extends the batch-based monitoring system by continuously sending data, mimicking real-world network traffic.

## How It Works
- Reads data from: 04_monitoring/data/current_batches/new_data.csv
- Processes data row-by-row
- Sends each record with a 1-second delay
- Simulates real-time streaming behavior

## Time Configuration
The pipeline uses Europe/Zurich (Switzerland timezone) to align with deployment region and handle daylight saving time.

## How to Run
cd 05_streaming
python streaming_pipeline.py

## Streaming Flow
Batch Data → Streaming Simulation → Model → Monitoring

## Purpose
- Demonstrate real-time data processing
- Extend batch pipeline into streaming context
- Simulate production-like behavior

## Example Output
[2026-05-23 14:40:10+02:00] Sending data row 1
[2026-05-23 14:40:11+02:00] Sending data row 2

## Note
This is a simulation. In real-world systems, streaming is implemented using tools like Kafka or Spark Streaming.

## Conclusion
This module adds real-time capability to the MLOps pipeline and demonstrates how streaming integrates with monitoring and prediction systems.
