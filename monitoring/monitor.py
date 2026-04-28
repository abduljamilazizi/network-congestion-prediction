import subprocess
import sys


def run_step(script_path):
    print(f"Running {script_path} ...")
    subprocess.run([sys.executable, script_path], check=True)


def main():
    run_step("monitoring/prepare_reference.py")
    run_step("monitoring/generate_batch.py")
    run_step("monitoring/calculate_metrics.py")
    run_step("monitoring/detect_data_drift.py")
    run_step("monitoring/detect_prediction_drift.py")
    run_step("monitoring/detect_performance_drift.py")
    print("Full monitoring and drift pipeline completed successfully.")


if __name__ == "__main__":
    main()