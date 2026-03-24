from fastapi import FastAPI

print("Network Congestion Prediction Project Started")

app = FastAPI(title="Network Congestion Prediction API")

@app.get("/")
def home():
    return {"message": "Network Congestion Prediction Project Started"}