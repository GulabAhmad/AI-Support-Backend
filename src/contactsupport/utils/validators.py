"""
Utility functions for validation.
"""
import re
from typing import Optional
from fastapi import HTTPException, status


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_support_message_data(name: str, email: str, message: str) -> None:
    """
    Validate support message data.
    
    Args:
        name: Customer name
        email: Customer email
        message: Support message
        
    Raises:
        HTTPException: If validation fails
    """
    if not name or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name is required and cannot be empty"
        )
    
    if not email or not email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required and cannot be empty"
        )
    
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    if not message or not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required and cannot be empty"
        )
    
    if len(message) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is too long. Maximum length is 10000 characters"
        )

