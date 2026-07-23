"""
ARIS - Automated Responsive Intelligence System
Free Text-based version (using free Hugging Face API)
No API keys needed, no quota limits!
"""

import os
from dotenv import load_dotenv
from core.ai_engine_free import AIEngine
from core.command_parser import CommandParser
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

class ARIS:
    """Main ARIS system controller - Free version"""
    
    def __init__(self):
        """Initialize ARIS system"""
        self.name = os.getenv('SYSTEM_NAME', 'ARIS')
        self.ai_engine = AIEngine()
        self.command_parser = CommandParser()
        logger.info(f"{self.name} system initialized (Free Mode)")
    
    def start(self):
        """Start the ARIS system in text mode"""
        logger.info(f"Starting {self.name} (Free Mode)...")
        print(f"\n{'='*60}")
        print(f"{self.name} - Automated Responsive Intelligence System")
        print(f"{'='*60}")
        print(f"FREE Version (No API keys needed!)")
        print(f"Type 'help' for commands or 'quit' to exit")
        print(f"{'='*60}\n")
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n{self.name}> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    logger.info("Shutdown initiated")
                    print(f"{self.name}: Shutting down. Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                logger.info(f"Command received: {user_input}")
                self.process_command(user_input)
                
            except KeyboardInterrupt:
                logger.info("Shutdown initiated")
                print(f"\n{self.name}: Shutting down. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                print(f"{self.name}: An error occurred. Please try again.")
    
    def process_command(self, command):
        """Process a voice command"""
        try:
            # Parse the command
            parsed = self.command_parser.parse(command)
            
            # Get AI response
            response = self.ai_engine.get_response(command)
            
            # Print response
            print(f"\n{self.name}: {response}\n")
            
            # Execute action if needed
            if parsed.get('action'):
                self.execute_action(parsed)
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            print(f"{self.name}: I couldn't process that command.")
    
    def execute_action(self, parsed_command):
        """Execute system actions based on parsed commands"""
        action = parsed_command.get('action')
        params = parsed_command.get('params', {})
        
        logger.info(f"Executing action: {action}")
        
        # Actions will be implemented in respective modules
        if action == 'open_app':
            from modules.system_module import open_application
            result = open_application(params.get('app_name'))
            print(f"{self.name}: {result}")
        elif action == 'get_weather':
            from modules.web_module import get_weather
            result = get_weather(params.get('location', 'current'))
            print(f"{self.name}: {result}")
        elif action == 'open_youtube':
            from modules.web_module import open_youtube
            result = open_youtube(params.get('query'))
            print(f"{self.name}: {result}")
        elif action == 'control_media':
            from modules.media_module import control_media
            result = control_media(params.get('action'), params.get('device'))
            print(f"{self.name}: {result}")
    
    def print_help(self):
        """Print help information"""
        help_text = f"""
{self.name} Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 General:
  • help                    - Show this help message
  • quit                    - Exit ARIS
  • Any question or command - Ask ARIS anything!

🎬 Examples:
  • "Tell me a joke"
  • "Who are you?"
  • "What can you do?"
  • "What's the time?"
  • "Open YouTube"
  • "Open Chrome"

💡 Try asking:
  • "Hello"
  • "Tell me something interesting"
  • "What is AI?"
  • "Help me learn about Python"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: This is the FREE version using Hugging Face API.
No API keys or quota limits needed!
"""
        print(help_text)

def main():
    """Entry point"""
    try:
        aris = ARIS()
        aris.start()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Failed to start ARIS: {str(e)}")

if __name__ == "__main__":
    main()
