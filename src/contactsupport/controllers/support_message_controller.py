"""
Controller for SupportMessage business logic.
Handles CRUD operations and business rules.
"""
from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models import SupportMessage, SupportMessageCreate, SupportMessageUpdate
from ..utils import validate_support_message_data, generate_ai_response


class SupportMessageController:
    """Controller for SupportMessage operations."""
    
    @staticmethod
    async def create_support_message(
        session: Session,
        message_data: SupportMessageCreate
    ) -> SupportMessage:
        """
        Create a new support message with AI-generated response.
        
        This method:
        1. Validates the input data
        2. Creates a new support message record
        3. Generates an AI response using the AI agent
        4. Updates the record with the AI response
        5. Returns the complete message with AI response
        
        Args:
            session: Database session
            message_data: Support message data
            
        Returns:
            Created SupportMessage instance with AI response
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate input data
        validate_support_message_data(
            message_data.name,
            message_data.email,
            message_data.message
        )
        
        # Create new support message (without AI response initially)
        support_message = SupportMessage(
            name=message_data.name,
            email=message_data.email,
            message=message_data.message
        )
        
        session.add(support_message)
        session.commit()
        session.refresh(support_message)
        
        # Generate AI response asynchronously
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("🤖 Starting AI response generation...")
            logger.info(f"   Message: {message_data.message[:100]}...")
            
            ai_response = await generate_ai_response(
                user_message=message_data.message,
                customer_name=message_data.name,
                customer_email=message_data.email
            )
            
            logger.info(f"📝 AI response received (length: {len(ai_response) if ai_response else 0})")
            logger.info(f"   Response preview: {ai_response[:100] if ai_response else 'None'}...")
            
            # Update the support message with AI response
            support_message.ai_response = ai_response
            session.add(support_message)
            session.commit()
            session.refresh(support_message)
            
            logger.info("✅ AI response saved to database")
            
        except Exception as e:
            # Log error but don't fail the request
            # The message is already saved, AI response can be added later
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"❌ Failed to generate AI response: {str(e)}")
            logger.exception(e)
            # Continue without AI response - it can be generated later
        
        return support_message
    
    @staticmethod
    def get_support_message(
        session: Session,
        message_id: int
    ) -> SupportMessage:
        """
        Get a support message by ID.
        
        Args:
            session: Database session
            message_id: Support message ID
            
        Returns:
            SupportMessage instance
            
        Raises:
            HTTPException: If message not found
        """
        statement = select(SupportMessage).where(SupportMessage.id == message_id)
        support_message = session.exec(statement).first()
        
        if not support_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Support message with ID {message_id} not found"
            )
        
        return support_message
    
    @staticmethod
    def get_all_support_messages(
        session: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[SupportMessage]:
        """
        Get all support messages with pagination.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of SupportMessage instances
        """
        statement = select(SupportMessage).offset(skip).limit(limit)
        support_messages = session.exec(statement).all()
        return list(support_messages)
    
    @staticmethod
    def update_support_message(
        session: Session,
        message_id: int,
        message_data: SupportMessageUpdate
    ) -> SupportMessage:
        """
        Update a support message.
        
        Args:
            session: Database session
            message_id: Support message ID
            message_data: Updated support message data
            
        Returns:
            Updated SupportMessage instance
            
        Raises:
            HTTPException: If message not found or validation fails
        """
        support_message = SupportMessageController.get_support_message(
            session, message_id
        )
        
        # Update fields if provided
        update_data = message_data.model_dump(exclude_unset=True)
        
        if "name" in update_data or "email" in update_data or "message" in update_data:
            name = update_data.get("name", support_message.name)
            email = update_data.get("email", support_message.email)
            message = update_data.get("message", support_message.message)
            
            validate_support_message_data(name, email, message)
        
        for key, value in update_data.items():
            setattr(support_message, key, value)
        
        session.add(support_message)
        session.commit()
        session.refresh(support_message)
        
        return support_message
    
    @staticmethod
    def delete_support_message(
        session: Session,
        message_id: int
    ) -> None:
        """
        Delete a support message.
        
        Args:
            session: Database session
            message_id: Support message ID
            
        Raises:
            HTTPException: If message not found
        """
        support_message = SupportMessageController.get_support_message(
            session, message_id
        )
        
        session.delete(support_message)
        session.commit()
    
    @staticmethod
    def get_support_messages_by_email(
        session: Session,
        email: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SupportMessage]:
        """
        Get all support messages by email address.
        
        Args:
            session: Database session
            email: Email address to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of SupportMessage instances
        """
        statement = (
            select(SupportMessage)
            .where(SupportMessage.email == email)
            .offset(skip)
            .limit(limit)
        )
        support_messages = session.exec(statement).all()
        return list(support_messages)

