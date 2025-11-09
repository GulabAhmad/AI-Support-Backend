"""
Database configuration and connection setup.
Handles database connection using SQLModel and PostgreSQL.
Supports both DATABASE_URL and individual environment variables.
"""
import os
import re
import logging
from typing import Generator, Optional
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


def clean_database_url(url: str) -> str:
    """
    Clean database URL by removing command prefixes and extra quotes.
    
    Args:
        url: Database URL that may contain psql command or quotes
        
    Returns:
        Cleaned database URL
    """
    # Remove 'psql' command prefix if present
    url = re.sub(r'^psql\s+', '', url, flags=re.IGNORECASE)
    
    # Remove single or double quotes
    url = url.strip("'\"")
    
    # Remove any leading/trailing whitespace
    url = url.strip()
    
    return url


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        # Check if DATABASE_URL is provided (takes precedence)
        database_url = os.getenv("DATABASE_URL")
        
        if database_url:
            # Clean the URL in case it has command prefixes or quotes
            database_url = clean_database_url(database_url)
            self._database_url = database_url
            logger.info("Using DATABASE_URL from environment variable")
        else:
            # Fall back to individual environment variables
            self.db_user: str = os.getenv("DB_USER", "postgres")
            self.db_password: str = os.getenv("DB_PASSWORD", "")
            self.db_host: str = os.getenv("DB_HOST", "localhost")
            self.db_port: str = os.getenv("DB_PORT", "5432")
            self.db_name: str = os.getenv("DB_NAME", "contactsupport")
            self._database_url = None
            logger.info("Using individual database environment variables")
        
    @property
    def database_url(self) -> str:
        """Get database URL from environment variables or construct it."""
        if self._database_url:
            return self._database_url
        else:
            # Construct URL from individual variables
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def create_engine(self, echo: bool = False) -> Engine:
        """Create and return database engine."""
        url = self.database_url
        
        # Log connection info (without sensitive data)
        if self._database_url:
            # Mask password in URL for logging
            safe_url = re.sub(r':([^:@]+)@', ':****@', url)
            logger.info(f"Connecting to database: {safe_url}")
        else:
            logger.info(f"Connecting to database: {self.db_host}:{self.db_port}/{self.db_name}")
        
        return create_engine(
            url,
            echo=echo,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,   # Recycle connections after 1 hour
            connect_args={
                # These will be handled by the URL parameters if present
                # But we can add additional SSL args if needed
            }
        )


# Initialize database configuration
db_config = DatabaseConfig()

# Create engine instance (lazy initialization)
_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Get or create database engine instance."""
    global _engine
    if _engine is None:
        _engine = db_config.create_engine(echo=False)
    return _engine


def init_db() -> bool:
    """
    Initialize database by creating all tables.
    
    Returns:
        True if initialization was successful, False otherwise
    """
    try:
        # Import models to register them with SQLModel metadata
        from ..models.support_message import SupportMessage
        
        engine = get_engine()
        logger.info("Attempting to connect to database and create tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully!")
        return True
    except OperationalError as e:
        logger.warning(
            f"Failed to connect to database: {str(e)}. "
            "The application will start, but database operations will fail. "
            "Please ensure PostgreSQL is running and the database credentials are correct."
        )
        return False
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {str(e)}")
        return False


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
        except OperationalError as e:
            logger.error(f"Database connection error: {str(e)}")
            session.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            session.rollback()
            raise

