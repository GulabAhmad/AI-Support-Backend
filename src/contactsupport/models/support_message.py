"""
SupportMessage model definition.
Represents a support message with AI response.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy import func


class SupportMessage(SQLModel, table=True):
    """
    SupportMessage model for storing customer support messages.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        name: Customer's name
        email: Customer's email address
        message: Customer's support message
        ai_response: AI-generated response to the message
        created_at: Timestamp when the message was created
    """
    __tablename__ = "support_message"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    email: str = Field(max_length=255, nullable=False, index=True)
    message: str = Field(nullable=False)
    ai_response: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


class SupportMessageCreate(SQLModel):
    """Schema for creating a new support message."""
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    message: str


class SupportMessageUpdate(SQLModel):
    """Schema for updating a support message."""
    name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    message: Optional[str] = Field(default=None)
    ai_response: Optional[str] = Field(default=None)


class SupportMessageResponse(SQLModel):
    """Schema for support message response."""
    id: int
    name: str
    email: str
    message: str
    ai_response: Optional[str]
    created_at: datetime

