"""
Command Parser Module
Parses and routes voice commands to appropriate handlers
"""

import re
from utils.logger import setup_logger

logger = setup_logger(__name__)

class CommandParser:
    """Parses voice commands and extracts intent and parameters"""
    
    def __init__(self):
        """Initialize command parser with command patterns"""
        self.commands = {
            'open_app': [
                r'open\s+(\w+)',
                r'launch\s+(\w+)',
                r'start\s+(\w+)'
            ],
            'get_weather': [
                r'weather',
                r'what\'s the weather',
                r'how\'s the weather'
            ],
            'open_youtube': [
                r'open youtube',
                r'youtube',
                r'search youtube for\s+(.+)',
                r'play\s+(.+)\s+on youtube'
            ],
            'control_media': [
                r'play',
                r'pause',
                r'next',
                r'previous',
                r'stop music'
            ],
            'make_call': [
                r'call\s+(\w+)',
                r'phone call to\s+(\w+)',
                r'dial\s+(\w+)'
            ],
            'send_message': [
                r'send\s+(\w+)\s+a message',
                r'text\s+(\w+)',
                r'message\s+(\w+)'
            ],
            'set_reminder': [
                r'remind me to\s+(.+)',
                r'set reminder\s+(.+)',
                r'remind me at\s+(.+)'
            ],
            'tell_time': [
                r'what time is it',
                r'tell me the time',
                r'current time'
            ],
            'tell_date': [
                r'what\'s the date',
                r'tell me the date',
                r'today\'s date'
            ]
        }
        
        logger.info("Command Parser initialized")
    
    def parse(self, command_text):
        """
        Parse a command and extract intent and parameters
        
        Args:
            command_text (str): Raw voice command text
        
        Returns:
            dict: Parsed command with action and parameters
        """
        try:
            command_text = command_text.lower().strip()
            logger.info(f"Parsing command: {command_text}")
            
            # Remove common prefixes
            command_text = re.sub(r'^(aris|alexa|hey|ok|please|can you)\s+', '', command_text)
            
            # Check each command type
            for action, patterns in self.commands.items():
                for pattern in patterns:
                    match = re.search(pattern, command_text, re.IGNORECASE)
                    if match:
                        params = {}
                        
                        # Extract parameters from regex groups
                        if match.groups():
                            if action == 'open_app':
                                params['app_name'] = match.group(1)
                            elif action == 'open_youtube':
                                params['query'] = match.group(1) if match.lastindex >= 1 else None
                            elif action == 'make_call':
                                params['contact'] = match.group(1)
                            elif action == 'send_message':
                                params['contact'] = match.group(1)
                            elif action == 'set_reminder':
                                params['reminder_text'] = match.group(1)
                        
                        result = {
                            'action': action,
                            'params': params,
                            'raw_command': command_text
                        }
                        
                        logger.info(f"Parsed as {action}: {result}")
                        return result
            
            # If no specific command matched, return as general query
            logger.info("No specific command pattern matched, treating as general query")
            return {
                'action': None,
                'params': {},
                'raw_command': command_text
            }
            
        except Exception as e:
            logger.error(f"Error parsing command: {str(e)}")
            return {
                'action': None,
                'params': {},
                'raw_command': command_text
            }
