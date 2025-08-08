from fastapi import FastAPI
from app.entrypoints.http.routes import api_router

app = FastAPI(title="Social API - Live Coding")

app.include_router(api_router)

# Health
@app.get("/health")
def health():
    return {"status": "ok"}
