"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.api.v1.scenarios import router as scenarios_router

app = FastAPI(
    title="Volkswagen Scenario Management System",
    description="OpenSCENARIO 2.0 test scenario generation and management platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scenarios_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized successfully")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Volkswagen Scenario Management System",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}