from prefect.schedules import Cron
from batch.train_predict_scheduled import network_congestion_batch_predict

if __name__ == "__main__":
    network_congestion_batch_predict.serve(
        name="network-congestion-daily",
        schedule=Cron("0 10 * * *", timezone="Europe/Berlin"),
    )