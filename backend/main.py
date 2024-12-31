from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.init_db import init_db, verify_database, reset_database, check_table_structure
import asyncio

app = FastAPI(
    title="Mental Health Journal Analysis API",
    description="API for analyzing personal journal entries using AI/ML",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Initialize the database on startup"""
    try:
        print("\n=== Starting Application ===")
        print("Performing complete database reset...")
        # Direct synchronous calls
        reset_database()
        check_table_structure()
        print("=== Startup Complete ===\n")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise e

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}