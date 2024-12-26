from fastapi import FastAPI
from .api.endpoints import upload

app = FastAPI()
app.include_router(upload.router, prefix="/api") 