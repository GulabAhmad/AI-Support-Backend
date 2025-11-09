"""
Database initialization script.
Creates the SupportMessage table in the database.
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from contactsupport.config import init_db
from contactsupport.models import SupportMessage


def create_tables():
    """Create all database tables."""
    print("Initializing database...")
    success = init_db()
    if success:
        print("Database initialized successfully!")
        print("Table 'support_message' has been created.")
    else:
        print("ERROR: Failed to initialize database.")
        print("Please ensure:")
        print("1. PostgreSQL is running")
        print("2. Database credentials in .env file are correct")
        print("3. Database 'contactsupport' exists")
        sys.exit(1)


if __name__ == "__main__":
    create_tables()

