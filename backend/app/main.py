from fastapi import FastAPI
from .db.init_db import init_db
from .api.endpoints import upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

# Include your routers here
app.include_router(upload.router) 

@app.get("/")
async def root():
    return {"message": "Journal Analyzer API is running"} 