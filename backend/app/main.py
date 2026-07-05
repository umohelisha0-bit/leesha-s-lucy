"""Main FastAPI application"""
import logging
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db, close_db
from app.api import calls, ai, analytics
from app.ws.handlers import call_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Closing database connections...")
    await close_db()
    logger.info("Application shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="Leesha's Lucy - AI Video Call API",
    description="Advanced AI video call software with realistic avatars",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "lucy-ai-backend",
        "version": "1.0.0"
    }


# Include API routers
app.include_router(calls.router, prefix="/api/calls", tags=["Calls"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Services"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


# WebSocket endpoint for video calls
@app.websocket("/ws/call/{call_id}/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, call_id: str, connection_id: str):
    """WebSocket endpoint for real-time call communication"""
    await call_handler(websocket, call_id, connection_id)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Leesha's Lucy AI Video Call API",
        "docs": "/docs",
        "version": "1.0.0",
        "features": [
            "Real-time video calling",
            "AI-powered conversations",
            "Emotion detection",
            "Realistic avatars",
            "No time limits",
            "No watermarks"
        ]
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )
