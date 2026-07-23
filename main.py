"""
ARIS - Automated Responsive Intelligence System
Main entry point for the ARIS AI assistant
"""

import os
from dotenv import load_dotenv
from core.ai_engine import AIEngine
from core.voice_handler import VoiceHandler
from core.command_parser import CommandParser
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

class ARIS:
    """Main ARIS system controller"""
    
    def __init__(self):
        """Initialize ARIS system"""
        self.name = os.getenv('SYSTEM_NAME', 'ARIS')
        self.ai_engine = AIEngine()
        self.voice_handler = VoiceHandler()
        self.command_parser = CommandParser()
        logger.info(f"{self.name} system initialized")
    
    def start(self):
        """Start the ARIS system"""
        logger.info(f"Starting {self.name}...")
        self.voice_handler.speak(f"{self.name} online. How can I assist you?")
        
        while True:
            try:
                # Listen for voice command
                logger.info("Listening for command...")
                command = self.voice_handler.listen()
                
                if command:
                    logger.info(f"Command received: {command}")
                    self.process_command(command)
                
            except KeyboardInterrupt:
                logger.info("Shutdown initiated")
                self.voice_handler.speak("Shutting down. Goodbye.")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                self.voice_handler.speak("An error occurred. Please try again.")
    
    def process_command(self, command):
        """Process a voice command"""
        try:
            # Parse the command
            parsed = self.command_parser.parse(command)
            
            # Get AI response
            response = self.ai_engine.get_response(command)
            
            # Execute command if needed
            if parsed.get('action'):
                self.execute_action(parsed)
            
            # Speak response
            self.voice_handler.speak(response)
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            self.voice_handler.speak("I couldn't process that command.")
    
    def execute_action(self, parsed_command):
        """Execute system actions based on parsed commands"""
        action = parsed_command.get('action')
        params = parsed_command.get('params', {})
        
        logger.info(f"Executing action: {action}")
        
        # Actions will be implemented in respective modules
        if action == 'open_app':
            from modules.system_module import open_application
            open_application(params.get('app_name'))
        elif action == 'get_weather':
            from modules.web_module import get_weather
            return get_weather(params.get('location', 'current'))
        elif action == 'open_youtube':
            from modules.web_module import open_youtube
            open_youtube(params.get('query'))
        elif action == 'control_media':
            from modules.media_module import control_media
            control_media(params.get('action'), params.get('device'))

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
