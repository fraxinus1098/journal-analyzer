from fastapi import FastAPI
from .db.init_db import init_db
from .api.endpoints import upload

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# Include your routers here
app.include_router(upload.router) 