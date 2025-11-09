"""
Main FastAPI application.
Entry point for the Contact Support API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from .config import init_db
from .routes import support_message_router
from .middleware import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)
# Import models to ensure they're registered
from .models import SupportMessage

# Create FastAPI application
app = FastAPI(
    title="Contact Support API",
    description="API for managing customer support messages with AI responses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(support_message_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    success = init_db()
    if success:
        pass
    else:
        pass
    
    # Initialize AI agent and check configuration
    try:
        from .utils.ai_agent import get_ai_agent, get_gemini_api_key
        gemini_key = get_gemini_api_key()
        if gemini_key:
            agent = get_ai_agent()
            if agent.gemini_client:
                pass
            else:
                pass
        else:
            pass
    except Exception as e:
        pass


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Contact Support API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Checks if the application and database are running.
    """
    from sqlalchemy import text
    from sqlalchemy.exc import OperationalError
    from .config import get_engine
    
    health_status = {
        "status": "healthy",
        "database": "unknown"
    }
    
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()  # Execute the query
        health_status["database"] = "connected"
    except OperationalError:
        health_status["database"] = "disconnected"
        health_status["status"] = "degraded"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status


@app.get("/health/ai", tags=["Health"])
async def ai_health_check():
    """
    AI service health check endpoint.
    Checks if AI services (Gemini) are configured and available.
    """
    from .utils.ai_agent import get_ai_agent, get_gemini_api_key
    
    ai_status = {
        "gemini": {
            "configured": False,
            "api_key_present": False,
            "client_initialized": False,
            "status": "unknown"
        }
    }
    
    # Check Gemini
    gemini_key = get_gemini_api_key()
    ai_status["gemini"]["api_key_present"] = gemini_key is not None and len(gemini_key) > 0
    if ai_status["gemini"]["api_key_present"]:
        ai_status["gemini"]["api_key_length"] = len(gemini_key)
        ai_status["gemini"]["api_key_preview"] = f"{gemini_key[:10]}...{gemini_key[-5:]}"
    
    # Check agent initialization
    try:
        agent = get_ai_agent()
        ai_status["gemini"]["client_initialized"] = agent.gemini_client is not None
        ai_status["gemini"]["configured"] = ai_status["gemini"]["client_initialized"]
        
        if ai_status["gemini"]["client_initialized"]:
            ai_status["gemini"]["status"] = "ready"
        elif ai_status["gemini"]["api_key_present"]:
            ai_status["gemini"]["status"] = "api_key_found_but_client_not_initialized"
        else:
            ai_status["gemini"]["status"] = "api_key_not_found"
            
    except Exception as e:
        ai_status["gemini"]["status"] = f"error: {str(e)}"
        ai_status["error"] = str(e)
    
    return ai_status

