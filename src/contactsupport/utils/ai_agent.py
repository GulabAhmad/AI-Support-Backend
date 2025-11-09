"""
AI Agent Module for Customer Support
Uses the agents library with Gemini API for response generation.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

# Mock response when API key is missing
MOCK_RESPONSE = "Thank you for your message. Our support team will reach out shortly."


def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from environment."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        # Strip whitespace and remove quotes if present
        key = key.strip().strip('"').strip("'")
    return key if key else None


def _get_client_and_model():
    """
    Get or create the Gemini client and model.
    
    Returns:
        Tuple of (external_client, model, config) or (None, None, None) if API key is not available
    """
    gemini_api_key = get_gemini_api_key()
    
    if not gemini_api_key:
        return None, None, None
    
    try:
        # Reference: https://ai.google.dev/gemini-api/docs/openai
        external_client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        
        model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client
        )
        
        config = RunConfig(
            model=model,
            model_provider=external_client,
            tracing_disabled=True
        )
        
        return external_client, model, config
    except Exception as e:
        print(f"Error creating Gemini client: {str(e)}")
        return None, None, None


def _get_agent(model) -> Optional[Agent]:
    """
    Get or create the AI agent instance.
    
    Args:
        model: The model to use for the agent
        
    Returns:
        Agent instance or None if model is not available
    """
    if not model:
        return None
    
    try:
        # Create agent with customer support instructions
        agent = Agent(
            name="CustomerSupportAssistant",
            instructions="""You are an AI customer support agent.

Your ONLY job is to answer Frequently Asked Questions (FAQs)
about our company's products and services.

Do not answer unrelated questions.
If you don't know, politely say: "I'm sorry, I can only help with product FAQs."

Always reply professionally, clearly, and briefly.

When answering questions:
- Be helpful and empathetic
- Provide clear, concise answers
- If the question matches a common FAQ, use that information
- Keep responses brief (2-3 sentences)""",
            model=model
        )
        
        return agent
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        return None


async def generate_ai_response(
    user_message: str,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    context: Optional[str] = None
) -> str:
    """
    Generate an AI-powered response to a customer support message.
    
    First checks FAQ knowledge base, then uses Gemini AI if no match found.
    
    Args:
        user_message: The customer's support message
        customer_name: Optional customer name for personalization
        customer_email: Optional customer email
        context: Optional additional context
        
    Returns:
        AI-generated response text
    """
    try:
        # First, check if there's a matching FAQ in the knowledge base
        from .faq_knowledge_base import find_matching_faq, format_faqs_for_prompt
        
        matching_faq = find_matching_faq(user_message)
        
        if matching_faq:
            answer = matching_faq['answer']
            
            # Personalize the answer if customer name is provided
            if customer_name:
                # Capitalize first letter of answer if it's not already capitalized
                if answer and answer[0].islower():
                    answer = answer[0].upper() + answer[1:]
                answer = f"Hi {customer_name}, {answer}"
            
            return answer
        
        # No FAQ match found, use AI agent
        external_client, model, config = _get_client_and_model()
        
        if not model or not config:
            return MOCK_RESPONSE
        
        agent = _get_agent(model)
        
        if not agent:
            return MOCK_RESPONSE
        
        # Build the prompt with context and FAQs
        prompt_parts = []
        
        # Add FAQ knowledge base to prompt
        faq_text = format_faqs_for_prompt()
        prompt_parts.append("FREQUENTLY ASKED QUESTIONS (FAQs):")
        prompt_parts.append("=" * 60)
        prompt_parts.append("Use the following FAQs as reference when answering questions:")
        prompt_parts.append(faq_text)
        prompt_parts.append("=" * 60)
        prompt_parts.append("\nCUSTOMER QUESTION:")
        prompt_parts.append("=" * 60)
        
        if customer_name:
            prompt_parts.append(f"Customer Name: {customer_name}")
        
        if customer_email:
            prompt_parts.append(f"Customer Email: {customer_email}")
        
        if context:
            prompt_parts.append(f"Additional Context: {context}")
        
        prompt_parts.append(f"\nCustomer Question: {user_message}")
        prompt_parts.append("\n" + "=" * 60)
        prompt_parts.append(
            "Please provide a helpful, professional, and clear response to this FAQ. "
            "If the question matches one of the FAQs above, use that answer as a reference. "
            "If this is not a product/service FAQ, politely decline. "
            "Keep your response brief (2-3 sentences) and directly address the question."
        )
        
        full_prompt = "\n".join(prompt_parts)
        
        # Run the agent
        result = await Runner.run(agent, full_prompt, run_config=config)
        
        # Extract response
        if result and hasattr(result, 'final_output') and result.final_output:
            response = str(result.final_output).strip()
            if len(response) > 10:  # Valid response
                return response
        
        # If response is invalid, return mock
        return MOCK_RESPONSE
        
    except Exception as e:
        print(f"Error generating AI response: {str(e)}")
        import traceback
        traceback.print_exc()
        return MOCK_RESPONSE


def get_ai_agent():
    """
    Get the AI agent instance (for compatibility with existing code).
    
    Returns:
        AIAgent instance
    """
    return AIAgent()


# For backward compatibility
class AIAgent:
    """Wrapper class for backward compatibility."""
    
    def __init__(self):
        external_client, model, config = _get_client_and_model()
        self.agent = _get_agent(model) if model else None
        self.gemini_client = self.agent is not None
        self.openai_client = None
        self._model = model
        self._config = config
    
    async def generate_response(
        self,
        user_message: str,
        customer_name: Optional[str] = None,
        customer_email: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Generate response using the agent."""
        return await generate_ai_response(
            user_message, customer_name, customer_email, context
        )
