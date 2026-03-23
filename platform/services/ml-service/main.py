from fastapi import FastAPI
import pandas as pd # Проверка наличия библиотеки

app = FastAPI(title="Uzun Demir ML Service")

@app.get("/")
def ml_root():
    return {
        "status": "AI Brain Active", 
        "libraries": "Pandas/Sklearn loaded",
        "pandas_version": pd.__version__
    }
