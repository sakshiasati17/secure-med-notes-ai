from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.db.database import engine, Base
from api.routes import auth, patients, notes, ai

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Secure Medical Notes API",
    description="A secure, AI-powered clinical documentation platform for healthcare teams",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(notes.router)
app.include_router(ai.router)

@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Secure Medical Notes API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}