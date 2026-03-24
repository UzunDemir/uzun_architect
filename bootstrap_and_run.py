
import os
import subprocess

# --- КОНФИГУРАЦИЯ ЗАВИСИМОСТЕЙ ---
# Теперь мы четко разделяем, кому что нужно
REQUIREMENTS_MAP = {
    "api-gateway": "fastapi\nuvicorn\nhttpx\n",
    "ml-service": "fastapi\nuvicorn\nhttpx\npandas\nscikit-learn\n", # ML получает тяжелую артиллерию
    "user-service": "fastapi\nuvicorn\nsqlalchemy\n", # Сервис пользователей — работу с БД
    "default": "fastapi\nuvicorn\n"
}

# --- КОНТЕНТ ФАЙЛОВ ---

DOCKER_CONTENT = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

MAIN_PY_GATEWAY = """from fastapi import FastAPI
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
"""

MAIN_PY_ML = """from fastapi import FastAPI
import pandas as pd # Проверка наличия библиотеки

app = FastAPI(title="Uzun Demir ML Service")

@app.get("/")
def ml_root():
    return {
        "status": "AI Brain Active", 
        "libraries": "Pandas/Sklearn loaded",
        "pandas_version": pd.__version__
    }
"""

MAIN_PY_DEFAULT = """from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root(): return {"status": "Standard Service Active"}
"""

# --- СТРУКТУРА ---

STRUCTURE = {
    "platform/api-gateway": ["main.py", "Dockerfile", "requirements.txt"],
    "platform/services/user-service": ["main.py", "Dockerfile", "requirements.txt"],
    "platform/services/order-service": ["main.py", "Dockerfile", "requirements.txt"],
    "platform/services/ml-service": ["main.py", "Dockerfile", "requirements.txt"],
    "platform/shared/event_bus": ["__init__.py"],
    "platform/notebooks": ["research.ipynb"],
}

COMPOSE_CONTENT = """
services:
  api-gateway:
    build: ./platform/api-gateway
    ports: ["8000:8000"]
    networks: [ud-network]

  user-service:
    build: ./platform/services/user-service
    networks: [ud-network]

  ml-service:
    build: ./platform/services/ml-service
    networks: [ud-network]

networks:
  ud-network:
    driver: bridge
"""

def setup_platform():
    print("🛠  Шаг 1: Генерация изолированного кода...")
    for folder, files in STRUCTURE.items():
        os.makedirs(folder, exist_ok=True)

        # Определяем имя сервиса из пути
        service_key = folder.split('/')[-1]

        for file_name in files:
            file_path = os.path.join(folder, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                if file_name == "Dockerfile":
                    f.write(DOCKER_CONTENT)

                elif file_name == "requirements.txt":
                    # Берем специфичные зависимости или дефолтные
                    content = REQUIREMENTS_MAP.get(service_key, REQUIREMENTS_MAP["default"])
                    f.write(content)

                elif file_name == "main.py":
                    if service_key == "api-gateway": f.write(MAIN_PY_GATEWAY)
                    elif service_key == "ml-service": f.write(MAIN_PY_ML)
                    else: f.write(MAIN_PY_DEFAULT)

                else:
                    f.write(f"# Uzun Demir: {file_name}")

    print("📄 Шаг 2: Создание compose.yml...")
    with open("compose.yml", "w", encoding="utf-8") as f:
        f.write(COMPOSE_CONTENT.strip())

    print("🐳 Шаг 3: Сборка (теперь с разными слоями)...")
    try:
        # --build обязателен, чтобы Docker перечитал новые requirements.txt
        subprocess.run(["docker", "compose", "up", "--build", "-d"], check=True)
        print("\n✅ РАСПРЕДЕЛЕННАЯ ПЛАТФОРМА ЗАПУЩЕНА!")
        print("🔗 Тест связи: http://localhost:8000/check-ml")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    setup_platform()
