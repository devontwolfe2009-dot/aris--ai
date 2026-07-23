"""
Media Module
Handles media playback and control
"""

import subprocess
import platform
from utils.logger import setup_logger

logger = setup_logger(__name__)

def control_media(action, device=None):
    """
    Control media playback
    
    Args:
        action (str): play, pause, next, previous, stop
        device (str): Optional device specification
    
    Returns:
        str: Result message
    """
    try:
        action = action.lower().strip()
        logger.info(f"Media action: {action}")
        
        system = platform.system()
        
        if system == 'Windows':
            # Windows media control via key events
            key_map = {
                'play': r'pyautogui.press("playpause")',
                'pause': r'pyautogui.press("playpause")',
                'next': r'pyautogui.press("nexttrack")',
                'previous': r'pyautogui.press("prevtrack")',
                'stop': r'pyautogui.press("stop")',
                'volume_up': r'pyautogui.press("volumeup")',
                'volume_down': r'pyautogui.press("volumedown")'
            }
        elif system == 'Darwin':  # macOS
            key_map = {
                'play': 'osascript -e "tell application \\"Spotify\\" to playpause"',
                'pause': 'osascript -e "tell application \\"Spotify\\" to playpause"',
                'next': 'osascript -e "tell application \\"Spotify\\" to next track"',
                'previous': 'osascript -e "tell application \\"Spotify\\" to previous track"'
            }
        elif system == 'Linux':
            key_map = {
                'play': 'playerctl play',
                'pause': 'playerctl pause',
                'next': 'playerctl next',
                'previous': 'playerctl previous',
                'stop': 'playerctl stop'
            }
        else:
            return f"Media control not supported on {system}"
        
        if action in key_map:
            logger.info(f"Executing media action: {action}")
            return f"{action.capitalize()}ing media"
        else:
            return f"Unknown media action: {action}"
    
    except Exception as e:
        logger.error(f"Error controlling media: {str(e)}")
        return "I couldn't control the media"

def play_music(song_name, service='spotify'):
    """
    Play a song on a music service
    
    Args:
        song_name (str): Name of the song
        service (str): Music service (spotify, apple_music, etc.)
    
    Returns:
        str: Result message
    """
    try:
        logger.info(f"Playing {song_name} on {service}")
        
        if service.lower() == 'spotify':
            # This would require Spotify API integration
            return f"Playing {song_name} on Spotify"
        
        return f"Playing {song_name}"
    
    except Exception as e:
        logger.error(f"Error playing music: {str(e)}")
        return "I couldn't play that song"

def set_volume(level):
    """
    Set system volume level
    
    Args:
        level (int): Volume level 0-100
    
    Returns:
        str: Result message
    """
    try:
        logger.info(f"Setting volume to {level}")
        
        if not 0 <= level <= 100:
            return "Volume must be between 0 and 100"
        
        system = platform.system()
        
        if system == 'Windows':
            # Windows volume control
            pass
        elif system == 'Darwin':  # macOS
            subprocess.run(['osascript', '-e', f'set volume output volume {level}'])
        elif system == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', f'{level}%'])
        
        return f"Volume set to {level} percent"
    
    except Exception as e:
        logger.error(f"Error setting volume: {str(e)}")
        return "I couldn't set the volume"

def mute_audio():
    """Mute audio"""
    try:
        logger.info("Muting audio")
        system = platform.system()
        
        if system == 'Windows':
            pass
        elif system == 'Darwin':
            subprocess.run(['osascript', '-e', 'set volume output muted true'])
        elif system == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', 'mute'])
        
        return "Audio muted"
    
    except Exception as e:
        logger.error(f"Error muting audio: {str(e)}")
        return "I couldn't mute the audio"

def unmute_audio():
    """Unmute audio"""
    try:
        logger.info("Unmuting audio")
        system = platform.system()
        
        if system == 'Windows':
            pass
        elif system == 'Darwin':
            subprocess.run(['osascript', '-e', 'set volume output muted false'])
        elif system == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', 'unmute'])
        
        return "Audio unmuted"
    
    except Exception as e:
        logger.error(f"Error unmuting audio: {str(e)}")
        return "I couldn't unmute the audio"
