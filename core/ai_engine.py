"""
AI Engine Module
Handles OpenAI API integration and conversational responses
"""

import os
from openai import OpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AIEngine:
    """OpenAI-powered AI engine for ARIS"""
    
    def __init__(self):
        """Initialize AI engine with OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        self.conversation_history = []
        self.system_prompt = """You are ARIS (Automated Responsive Intelligence System), 
        a helpful AI assistant similar to Jarvis from Iron Man. You are intelligent, 
        witty, and capable of helping with a wide variety of tasks. Keep responses concise 
        and natural. When the user asks you to perform actions like opening applications, 
        making calls, or controlling devices, acknowledge that you're executing the command."""
        
        logger.info("AI Engine initialized with OpenAI GPT-4")
    
    def get_response(self, user_input, include_history=True):
        """
        Get a response from the AI engine
        
        Args:
            user_input (str): User's input message
            include_history (bool): Whether to include conversation history
        
        Returns:
            str: AI response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            if include_history:
                messages.extend(self.conversation_history)
            else:
                messages.append(self.conversation_history[-1])
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract response text
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            logger.info(f"AI Response generated: {assistant_message[:100]}...")
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return "I apologize, but I'm having trouble processing that request."
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def set_system_prompt(self, prompt):
        """Update the system prompt"""
        self.system_prompt = prompt
        logger.info("System prompt updated")
