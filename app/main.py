from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router
from app.web.routes import router as web_router
from app.services.storage_service import ensure_storage_directories

ensure_storage_directories()
app = FastAPI(title="PhotoTheme Factory Local", version="0.2.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/outputs", StaticFiles(directory="data/outputs"), name="outputs")
app.include_router(web_router)
app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok", "mode": "local-web-mock"}
