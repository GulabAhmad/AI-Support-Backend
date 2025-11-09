"""
Python script to execute SQL commands for database setup.
Executes the create_table.sql script using psycopg2.
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "contactsupport")
}


def execute_sql_file(sql_file_path: str):
    """
    Execute SQL commands from a file.
    
    Args:
        sql_file_path: Path to the SQL file
    """
    # Get the absolute path to the SQL file
    script_dir = Path(__file__).parent
    sql_file = script_dir / sql_file_path
    
    if not sql_file.exists():
        print(f"Error: SQL file not found at {sql_file}")
        sys.exit(1)
    
    # Read SQL file
    with open(sql_file, "r") as f:
        sql_commands = f.read()
    
    # Connect to database
    try:
        print(f"Connecting to database: {DB_CONFIG['dbname']} on {DB_CONFIG['host']}")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Executing SQL commands...")
        cursor.execute(sql_commands)
        
        print("SQL commands executed successfully!")
        print("Table 'support_message' has been created.")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def execute_custom_sql(sql_command: str):
    """
    Execute a custom SQL command.
    
    Args:
        sql_command: SQL command to execute
    """
    try:
        print(f"Connecting to database: {DB_CONFIG['dbname']} on {DB_CONFIG['host']}")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Executing SQL command...")
        cursor.execute(sql_command)
        
        print("SQL command executed successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Execute custom SQL command
        sql_command = sys.argv[1]
        execute_custom_sql(sql_command)
    else:
        # Execute SQL file
        execute_sql_file("create_table.sql")

