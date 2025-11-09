"""
Contact Support API
Main entry point for the application.
"""
from .main import app

__all__ = ["app"]


def main() -> None:
    """Main entry point for the application."""
    import uvicorn
    uvicorn.run(
        "contactsupport.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
