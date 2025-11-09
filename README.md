# Contact Support API

A RESTful API for managing customer support messages with AI response capabilities, built with FastAPI and PostgreSQL.

## Features

- ✅ RESTful API design
- ✅ Clean, modular architecture
- ✅ Proper error handling
- ✅ Database models using SQLModel
- ✅ Input validation
- ✅ Comprehensive API documentation

## Project Structure

```
contactsupport/
├── config/           # Database configuration
├── controllers/      # Business logic
├── middleware/       # Error handling middleware
├── models/           # Database models
├── routes/           # API routes
├── scripts/          # Database initialization scripts
├── utils/            # Utility functions
└── main.py           # Main FastAPI application
```

## Prerequisites

- Python 3.13+
- PostgreSQL database
- uv package manager (or pip)

## Installation

1. Clone the repository

2. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

3. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

4. Update the `.env` file with your database credentials:

**Option A: Using DATABASE_URL (Recommended for cloud databases):**
```env
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
```

**Example for Neon Database:**
```env
DATABASE_URL=postgresql://neondb_owner:password@ep-patient-forest-ahvawy8r-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Option B: Using individual environment variables:**
```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=contactsupport
```

> **Note:** DATABASE_URL takes precedence over individual variables. See [ENV_SETUP.md](ENV_SETUP.md) for detailed configuration options.

5. Create the database:
```bash
createdb contactsupport
```

## Database Setup

### Option 1: Using Python Script (Recommended)

Initialize the database using SQLModel:
```bash
python -m contactsupport.scripts.init_db
```

### Option 2: Using SQL Script

Execute the SQL script directly:
```bash
python -m contactsupport.scripts.execute_sql
```

Or execute the SQL file directly in PostgreSQL:
```bash
psql -U postgres -d contactsupport -f src/contactsupport/scripts/create_table.sql
```

### Option 3: Using Custom SQL Command

Execute a custom SQL command:
```bash
python -m contactsupport.scripts.execute_sql "CREATE TABLE IF NOT EXISTS support_message (...)"
```

## Running the Application

Start the development server:
```bash
uvicorn contactsupport.main:app --reload
# or
python -m contactsupport
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Support Messages

- `POST /api/support-messages/` - Create a new support message
- `GET /api/support-messages/` - Get all support messages (with pagination)
- `GET /api/support-messages/{message_id}` - Get a specific support message
- `GET /api/support-messages/email/{email}` - Get messages by email
- `PUT /api/support-messages/{message_id}` - Update a support message
- `DELETE /api/support-messages/{message_id}` - Delete a support message

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Example Request

Create a support message:
```bash
curl -X POST "http://localhost:8000/api/support-messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "I need help with my account"
  }'
```

## Database Schema

### SupportMessage Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| name | VARCHAR(255) | Customer name |
| email | VARCHAR(255) | Customer email (indexed) |
| message | TEXT | Support message |
| ai_response | TEXT | AI-generated response (nullable) |
| created_at | TIMESTAMP | Creation timestamp |

## Development

### Code Quality

The codebase follows these principles:

- Clean, modular code structure
- Separation of concerns
- Comprehensive error handling
- Input validation
- RESTful API design
- Well-documented code

### Testing

Run tests (when available):
```bash
pytest
```

## License

MIT License

## Author

Gulab Ahmad (gulabahmad724@gmail.com)

"# AI-Support-Backend" 
