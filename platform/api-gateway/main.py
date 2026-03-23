from fastapi import FastAPI
import httpx

app = FastAPI(title="Uzun Demir Gateway")

@app.get("/")
async def root():
    return {"message": "Gateway Online", "mode": "Distributed Dependencies"}

@app.get("/check-ml")
async def check_ml():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://ml-service:8000/")
        return {"gateway_response": "ML Contacted", "ml_data": response.json()}
