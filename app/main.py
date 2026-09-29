from fastapi import FastAPI

from app.api.routes import api_router
from app.core.storage.router import router as storage_router

app = FastAPI(title="Yefan Bridal API", version="1.0.0")


app.include_router(api_router)
app.include_router(storage_router)
