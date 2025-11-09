"""
FAQ Knowledge Base
Contains predefined FAQs and answers for the AI agent to reference.
"""
from typing import List, Dict, Optional
import re


# FAQ Knowledge Base
FAQ_DATABASE = [
    {
        "question": "How can I reset my password?",
        "answer": "Go to the login page and click 'Forgot Password'. You'll receive a reset email."
    },
    {
        "question": "What is your refund policy?",
        "answer": "We offer full refunds within 7 days of purchase if the product is defective."
    },
    {
        "question": "Do you offer 24/7 customer support?",
        "answer": "Yes, our AI and human agents are available 24/7 to assist you."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can contact our support team via the 'Contact Us' page or by emailing support@example.com."
    },
    {
        "question": "Can I change my registered email address?",
        "answer": "Yes, go to your account settings and update your email address, then verify the new one."
    },
    {
        "question": "How do I delete my account?",
        "answer": "To delete your account, go to Settings > Privacy > Delete Account. You'll receive a confirmation email."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept credit/debit cards, PayPal, and Stripe payments."
    },
    {
        "question": "Can I upgrade or downgrade my plan?",
        "answer": "Yes, you can change your subscription plan anytime from your account settings."
    },
    {
        "question": "Do you have a free trial?",
        "answer": "Yes, we offer a 7-day free trial for new users to explore all premium features."
    },
    {
        "question": "Is my data secure with your service?",
        "answer": "Absolutely. We use advanced encryption and follow strict data privacy standards to keep your data safe."
    },
    {
        "question": "Can I access the service from my mobile device?",
        "answer": "Yes, our platform is fully responsive and works seamlessly on all mobile devices."
    },
    {
        "question": "What should I do if I don't receive the password reset email?",
        "answer": "Please check your spam folder first. If you still can't find it, contact support to resend the link."
    },
    {
        "question": "How long does it take to process a refund?",
        "answer": "Refunds are usually processed within 3–5 business days after approval."
    },
    {
        "question": "Can multiple users share one account?",
        "answer": "For security reasons, sharing accounts is not recommended. Each user should have their own login."
    },
    {
        "question": "How can I update my billing information?",
        "answer": "Go to your account's Billing section and click 'Update Payment Details' to make changes."
    },
    {
        "question": "Do you send notifications about system updates?",
        "answer": "Yes, we notify all users via email and dashboard alerts whenever new updates are released."
    },
    {
        "question": "Can I pause my subscription temporarily?",
        "answer": "Currently, we don't offer subscription pauses, but you can cancel and reactivate anytime."
    },
    {
        "question": "Do you provide training or onboarding support?",
        "answer": "Yes, we offer video tutorials and live onboarding sessions for new customers."
    },
    {
        "question": "How can I cancel my subscription?",
        "answer": "You can cancel your subscription by going to your account settings and clicking 'Cancel Subscription'."
    },
    {
        "question": "How can I change my subscription plan?",
        "answer": "You can change your subscription plan by going to your account settings and clicking 'Change Subscription Plan'."
    },
    {
        "question": "How can I get a refund?",
        "answer": "You can request a refund by going to your account settings and clicking 'Request Refund'."
    },
    {
        "question": "How can I change my shipping address?",
        "answer": "You can change your shipping address by going to your account settings and clicking 'Change Shipping Address'."
    },
    {
        "question": "How can I change my billing information?",
        "answer": "You can change your billing information by going to your account settings and clicking 'Change Billing Information'."
    },
    {
        "question": "Do you offer any warranties on your products?",
        "answer": "Yes, we offer a 1-year warranty on all our products."
    },
    {
        "question": "What are your operating hours?",
        "answer": "We are open from 9:00 AM to 5:00 PM, Monday to Friday."
    },
    {
        "question": "How long is your warranty period?",
        "answer": "Our warranty period is 1 year from the date of purchase."
    },
    {
        "question": "How can I track my order?",
        "answer": "You can track your order by going to your account settings and clicking 'Track Order'."
    },
    {
        "question": " What payment methods do you accept? ",
        "answer": "We accept credit/debit cards, PayPal, and Stripe payments."
    },
    {
        "question": "How can I report a technical issue or bug?",
        "answer": "You can report any issue using the 'Report a Bug' button in your dashboard or contact support directly."
    },
    {
        "question": "Is there a way to export my data?",
        "answer": "Yes, you can export your account data from Settings > Data Export anytime."
    }
]


def find_matching_faq(user_question: str) -> Optional[Dict[str, str]]:
    """
    Find a matching FAQ from the knowledge base based on user question.
    
    Uses keyword matching and similarity scoring to find the best match.
    
    Args:
        user_question: The user's question
        
    Returns:
        Matching FAQ dict with question and answer, or None if no match found
    """
    user_question_lower = user_question.lower().strip()
    
    # Direct exact match (case-insensitive)
    for faq in FAQ_DATABASE:
        if faq["question"].lower().strip() == user_question_lower:
            return faq
    
    # Keyword-based matching
    best_match = None
    best_score = 0
    
    for faq in FAQ_DATABASE:
        faq_question_lower = faq["question"].lower()
        faq_answer_lower = faq["answer"].lower()
        
        # Extract keywords from FAQ question
        faq_keywords = set(re.findall(r'\b\w+\b', faq_question_lower))
        user_keywords = set(re.findall(r'\b\w+\b', user_question_lower))
        
        # Calculate similarity score
        common_keywords = faq_keywords.intersection(user_keywords)
        
        # Remove common stop words
        stop_words = {'i', 'my', 'me', 'you', 'your', 'the', 'a', 'an', 'is', 'are', 
                     'was', 'were', 'do', 'does', 'did', 'can', 'could', 'what', 
                     'how', 'where', 'when', 'why', 'who', 'which', 'this', 'that',
                     'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from'}
        
        common_keywords = common_keywords - stop_words
        
        if len(common_keywords) > 0:
            # Calculate score based on common keywords
            score = len(common_keywords) / max(len(faq_keywords - stop_words), 1)
            
            # Boost score if key phrases match
            key_phrases = [
                'reset password', 'forgot password', 'password reset',
                'refund policy', 'refund',
                '24/7', 'customer support', 'contact support',
                'change email', 'update email', 'email address',
                'delete account',
                'payment method', 'payment',
                'upgrade plan', 'downgrade plan', 'subscription',
                'free trial',
                'data secure', 'data security', 'privacy',
                'mobile device', 'mobile',
                'password reset email',
                'process refund', 'refund time',
                'share account',
                'billing information', 'update billing',
                'system updates', 'notifications',
                'pause subscription',
                'training', 'onboarding',
                'technical issue', 'bug', 'report bug',
                'export data'
            ]
            
            for phrase in key_phrases:
                if phrase in user_question_lower and phrase in faq_question_lower:
                    score += 0.3
                    break
            
            if score > best_score:
                best_score = score
                best_match = faq
    
    # Return match if score is above threshold
    if best_match and best_score >= 0.3:
        return best_match
    
    return None


def get_all_faqs() -> List[Dict[str, str]]:
    """
    Get all FAQs from the knowledge base.
    
    Returns:
        List of all FAQ dictionaries
    """
    return FAQ_DATABASE.copy()


def format_faqs_for_prompt() -> str:
    """
    Format FAQs for inclusion in AI prompt.
    
    Returns:
        Formatted string of FAQs
    """
    faq_text = "FREQUENTLY ASKED QUESTIONS (FAQs):\n"
    faq_text += "=" * 60 + "\n\n"
    
    for i, faq in enumerate(FAQ_DATABASE, 1):
        faq_text += f"{i}. Q: {faq['question']}\n"
        faq_text += f"   A: {faq['answer']}\n\n"
    
    return faq_text

