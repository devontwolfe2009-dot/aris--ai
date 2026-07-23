"""
AI Engine Module - Free Version
Uses Hugging Face API (free, no quota limits)
"""

import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AIEngine:
    """Free AI engine using Hugging Face Inference API"""
    
    def __init__(self):
        """Initialize AI engine with free Hugging Face API"""
        # Using free Hugging Face inference API
        self.api_url = "https://api-inference.huggingface.co/models/gpt2"
        self.conversation_history = []
        self.system_prompt = """You are ARIS (Automated Responsive Intelligence System), 
        a helpful AI assistant similar to Jarvis from Iron Man. You are intelligent, 
        witty, and capable of helping with a wide variety of tasks. Keep responses concise 
        and natural. When the user asks you to perform actions like opening applications, 
        making calls, or controlling devices, acknowledge that you're executing the command."""
        
        logger.info("AI Engine initialized with Free Hugging Face API (GPT-2)")
    
    def get_response(self, user_input, include_history=True):
        """
        Get a response from the AI engine using free API
        
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
            
            # Build context from history
            context = self.system_prompt + "\n\n"
            if include_history and len(self.conversation_history) > 1:
                for msg in self.conversation_history[:-1]:
                    if msg["role"] == "user":
                        context += f"User: {msg['content']}\n"
                    else:
                        context += f"Assistant: {msg['content']}\n"
            
            context += f"User: {user_input}\nAssistant:"
            
            # Call Hugging Face API
            logger.info(f"Calling Hugging Face API with input: {user_input[:50]}...")
            
            payload = {
                "inputs": context,
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    # Extract just the assistant's response
                    if 'Assistant:' in generated_text:
                        assistant_response = generated_text.split('Assistant:')[-1].strip()
                    else:
                        assistant_response = generated_text.replace(context, '').strip()
                    
                    # Clean up the response
                    assistant_response = assistant_response.split('\n')[0].strip()
                    
                    if not assistant_response or len(assistant_response) < 5:
                        assistant_response = self.generate_smart_response(user_input)
                    
                else:
                    assistant_response = self.generate_smart_response(user_input)
            else:
                logger.warning(f"API returned status {response.status_code}, using fallback")
                assistant_response = self.generate_smart_response(user_input)
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            logger.info(f"AI Response generated: {assistant_response[:100]}...")
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return self.generate_smart_response(user_input)
    
    def generate_smart_response(self, user_input):
        """Generate a smart response based on keywords when API fails"""
        user_lower = user_input.lower()
        
        # Joke responses
        if 'joke' in user_lower:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a fake noodle? An impasta!",
                "Why don't eggs tell jokes? They'd crack up!",
                "What did the ocean say to the beach? Nothing, it just waved!"
            ]
            import random
            return random.choice(jokes)
        
        # Who are you questions
        if any(x in user_lower for x in ['who are you', 'what are you', 'introduce yourself']):
            return "I'm ARIS, your Automated Responsive Intelligence System. I'm here to help you with tasks like opening applications, controlling devices, answering questions, and much more!"
        
        # Greeting responses
        if any(x in user_lower for x in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm ARIS. How can I assist you today?"
        
        # Weather (without API)
        if 'weather' in user_lower:
            return "I don't have access to weather data right now, but you could check a weather website or app for the latest information."
        
        # Time
        if any(x in user_lower for x in ['time', 'what time']):
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        # Date
        if any(x in user_lower for x in ['date', 'today']):
            from datetime import datetime
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}."
        
        # Help
        if 'help' in user_lower:
            return "I can help you with many things! Try asking me a question, requesting a joke, or telling me to open an application. Type 'help' in the main menu for more commands."
        
        # Default response
        default_responses = [
            "That's an interesting question! I'm still learning, but I'll do my best to help.",
            "I see what you mean. Let me think about that.",
            "That's a good point. How can I help you further?",
            "I understand. Is there anything else you'd like to know?",
            "Interesting! Tell me more about what you're looking for."
        ]
        import random
        return random.choice(default_responses)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def set_system_prompt(self, prompt):
        """Update the system prompt"""
        self.system_prompt = prompt
        logger.info("System prompt updated")
