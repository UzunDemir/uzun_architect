# 🏗️ Uzun Demir Distributed Platform

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)

<img width="1408" height="768" alt="Gemini_Generated_Image_whqex1whqex1whqe" src="https://github.com/user-attachments/assets/07ddce6c-f2ca-46e2-873a-927f2d313838" />

## 📋 Overview

A **distributed microservices platform** built with FastAPI and Docker Compose. Each service has isolated dependencies, enabling independent scaling and development. The platform demonstrates service discovery, inter-service communication, and containerized deployment.

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ API Gateway  │  │ ML Service   │  │ User Service │     │
│  │   :8000      │◄─┤   :8000      │  │   :8000      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                                                   │
│         └──────────► Order Service (future)                │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Services & Dependencies

| Service | Dependencies | Purpose |
|---------|--------------|---------|
| **API Gateway** | fastapi, uvicorn, httpx | Entry point, request routing |
| **ML Service** | fastapi, uvicorn, httpx, pandas, scikit-learn | AI/ML predictions |
| **User Service** | fastapi, uvicorn, sqlalchemy | User management |
| **Order Service** | fastapi, uvicorn | Order processing |

## 📁 Project Structure

```
uzun-platform/
├── compose.yml                    # Docker Compose configuration
├── platform/
│   ├── api-gateway/               # Entry point service
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt       # httpx only
│   │
│   ├── services/
│   │   ├── ml-service/            # AI/ML microservice
│   │   │   ├── main.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt   # pandas, scikit-learn
│   │   │
│   │   ├── user-service/          # User management
│   │   │   └── requirements.txt   # sqlalchemy
│   │   │
│   │   └── order-service/         # Order processing
│   │       └── requirements.txt   # minimal
│   │
│   ├── shared/
│   │   └── event_bus/             # Shared utilities
│   │       └── __init__.py
│   │
│   └── notebooks/                 # Research & experimentation
│       └── research.ipynb
```

## 🛠️ Installation & Setup

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.11 (for local development)

### Quick Start

```bash
# Clone repository
git clone https://github.com/UzunDemir/platform.git
cd platform

# Run the setup script
python setup_platform.py

# Or run Docker Compose directly
docker compose up --build -d
```

### Manual Setup

```bash
# Build all services
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## 🔗 Service Endpoints

| Service | Internal URL | External Access |
|---------|--------------|-----------------|
| API Gateway | http://api-gateway:8000 | http://localhost:8000 |
| ML Service | http://ml-service:8000 | Not exposed directly |
| User Service | http://user-service:8000 | Not exposed directly |

### API Endpoints

```bash
# Gateway health check
curl http://localhost:8000/

# Test ML service communication
curl http://localhost:8000/check-ml

# ML service direct (if needed)
curl http://localhost:8001/  # Not exposed by default

# ML prediction (POST)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "example"}'
```

## 🧪 Testing Inter-Service Communication

```python
# Via API Gateway
import httpx

response = httpx.get("http://localhost:8000/check-ml")
print(response.json())
# Output: {
#   "gateway_response": "ML Contacted",
#   "ml_data": {"status": "AI Brain Active", ...}
# }
```

## 📦 Dependency Isolation Strategy

Each service gets only the libraries it needs:

```python
# REQUIREMENTS_MAP controls dependencies per service
REQUIREMENTS_MAP = {
    "api-gateway": "fastapi\nuvicorn\nhttpx\n",        # Lightweight
    "ml-service": "fastapi\nuvicorn\nhttpx\npandas\nscikit-learn\n",  # Heavy
    "user-service": "fastapi\nuvicorn\nsqlalchemy\n",  # DB tools
    "default": "fastapi\nuvicorn\n"                    # Minimal
}
```

## 🐳 Docker Configuration

### Dockerfile (All Services)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Network
```yaml
services:
  api-gateway:
    build: ./platform/api-gateway
    ports: ["8000:8000"]
    networks: [ud-network]

  ml-service:
    build: ./platform/services/ml-service
    networks: [ud-network]  # Internal only

networks:
  ud-network:
    driver: bridge
```

## 🔧 Development

### Local Development (without Docker)

```bash
# Install dependencies for specific service
cd platform/services/ml-service
pip install -r requirements.txt

# Run service locally
uvicorn main:app --reload --port 8001
```

### Add New Service

1. Create directory in `platform/services/`
2. Add `main.py`, `Dockerfile`, `requirements.txt`
3. Update `STRUCTURE` dict in `setup_platform.py`
4. Add service to `compose.yml`

## 📊 Performance Considerations

| Service | Image Size | Build Time | Memory Usage |
|---------|------------|------------|--------------|
| API Gateway | ~150 MB | ~30s | ~100 MB |
| ML Service | ~250 MB | ~60s | ~300 MB |
| User Service | ~150 MB | ~30s | ~120 MB |

## 🚦 Troubleshooting

### Common Issues

**Service can't reach another service:**
```bash
# Check if services are running
docker compose ps

# Check network connectivity
docker exec -it platform-api-gateway-1 ping ml-service
```

**Dependency installation fails:**
```bash
# Rebuild with no cache
docker compose build --no-cache

# Check requirements.txt content
docker exec -it platform-ml-service-1 cat requirements.txt
```

**Port conflicts:**
```bash
# Change port mapping in compose.yml
ports: ["8000:8000"]  # [HOST:CONTAINER]
```

## 🔒 Security Notes

- Services communicate internally via Docker network
- Only API Gateway exposes ports to host
- No authentication implemented (add for production)
- Consider adding rate limiting and API keys

## 🎯 Future Enhancements

- [ ] Add service discovery (Consul/etcd)
- [ ] Implement API authentication (JWT)
- [ ] Add load balancer (Nginx/Traefik)
- [ ] Centralized logging (ELK stack)
- [ ] Distributed tracing (Jaeger)
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] Database migrations (Alembic)
- [ ] Health check endpoints
- [ ] Metrics collection (Prometheus)

## 📄 License

MIT License – free to use, modify, and distribute.

## 👨‍💻 Author

**Uzun Demir**
- GitHub: [@UzunDemir](https://github.com/UzunDemir)
- Telegram: [@ai_stack](https://t.me/ai_stack)
- LinkedIn: [Uzun Demir](https://www.linkedin.com/in/uzundemir/)

---

⭐ **Star this repo** if you find the microservices architecture useful!

*Built with 🐳 Docker and ⚡ FastAPI*
```
