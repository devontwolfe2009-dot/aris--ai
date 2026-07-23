"""
Voice Handler Module
Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceHandler:
    """Handles voice input and output for ARIS"""
    
    def __init__(self):
        """Initialize voice handler"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume 0-1
        
        logger.info("Voice Handler initialized")
    
    def listen(self, timeout=10):
        """
        Listen for voice input from microphone
        
        Args:
            timeout (int): Timeout in seconds
        
        Returns:
            str: Recognized text or None
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            logger.info("Processing audio...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error during listening: {str(e)}")
            return None
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to speak
        """
        try:
            logger.info(f"Speaking: {text[:100]}...")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error during speech synthesis: {str(e)}")
    
    def set_voice_rate(self, rate):
        """Set speech rate (50-300)"""
        self.engine.setProperty('rate', rate)
        logger.info(f"Voice rate set to {rate}")
    
    def set_voice_volume(self, volume):
        """Set voice volume (0.0-1.0)"""
        if 0 <= volume <= 1:
            self.engine.setProperty('volume', volume)
            logger.info(f"Voice volume set to {volume}")
        else:
            logger.warning(f"Invalid volume: {volume}")
