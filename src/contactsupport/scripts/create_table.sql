-- SQL script to create the SupportMessage table
-- This script can be executed directly in PostgreSQL

CREATE TABLE IF NOT EXISTS support_message (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    ai_response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster queries
CREATE INDEX IF NOT EXISTS idx_support_message_email ON support_message(email);

-- Create index on created_at for faster sorting
CREATE INDEX IF NOT EXISTS idx_support_message_created_at ON support_message(created_at);

