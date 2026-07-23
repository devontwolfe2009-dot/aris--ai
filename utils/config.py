"""
Configuration Module
Handles configuration management
"""

import os
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Config:
    """Configuration manager"""
    
    def __init__(self):
        """Load environment configuration"""
        load_dotenv()
        self._load_config()
    
    def _load_config(self):
        """Load all configuration"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.system_name = os.getenv('SYSTEM_NAME', 'ARIS')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info(f"Configuration loaded (Debug: {self.debug})")
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return getattr(self, key, default)
    
    def set(self, key, value):
        """Set a configuration value"""
        setattr(self, key, value)
        logger.info(f"Configuration updated: {key}={value}")
    
    def validate(self):
        """Validate required configuration"""
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not configured")
            return False
        return True

# Global config instance
config = Config()
