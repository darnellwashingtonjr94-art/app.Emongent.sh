from fastapi import FastAPI
from src.engine import ExecutionEngine

app = FastAPI(title="app.Emongent.sh API", version="1.0.0")
engine = ExecutionEngine()

@app.get("/health")
async def health_check():
    connected = await engine.client.check_connection()
    return {
        "status": "healthy",
        "network_connected": connected,
        "engine_active": engine.is_running
    }

@app.post("/engine/start")
async def start_engine():
    if not engine.is_running:
        return {"message": "Engine startup sequence triggered"}
    return {"message": "Engine is already running"}
