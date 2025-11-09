"""
Routes for SupportMessage API endpoints.
RESTful API design with proper error handling.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from ..config import get_session
from ..models import (
    SupportMessageCreate,
    SupportMessageResponse
)
from ..controllers import SupportMessageController

router = APIRouter(
    prefix="/api/support-messages",
    tags=["Support Messages"]
)


@router.post(
    "/",
    response_model=SupportMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new support message",
    description="Create a new support message with name, email, and message"
)
async def create_support_message(
    message_data: SupportMessageCreate,
    session: Session = Depends(get_session)
) -> SupportMessageResponse:
    """
    Create a new support message.
    
    Args:
        message_data: Support message data
        session: Database session
        
    Returns:
        Created support message
    """
    try:
        support_message = await SupportMessageController.create_support_message(
            session, message_data
        )
        return SupportMessageResponse.model_validate(support_message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create support message: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[SupportMessageResponse],
    summary="Get all support messages",
    description="Get all support messages with pagination"
)
async def get_all_support_messages(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    session: Session = Depends(get_session)
) -> List[SupportMessageResponse]:
    """
    Get all support messages with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        session: Database session
        
    Returns:
        List of support messages
    """
    try:
        support_messages = SupportMessageController.get_all_support_messages(
            session, skip, limit
        )
        return [
            SupportMessageResponse.model_validate(msg) 
            for msg in support_messages
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve support messages: {str(e)}"
        )

