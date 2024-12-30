from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.init_db import init_db, verify_database

app = FastAPI(
    title="Mental Health Journal Analysis API",
    description="API for analyzing personal journal entries using AI/ML",
    version="1.0.0"
)

# TODO: Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Update with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Initialize database
@app.on_event("startup")
async def startup_event():
    verify_database()

# TODO: Include API routers
app.include_router(api_router, prefix="/api/v1")

# TODO: Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}