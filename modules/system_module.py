"""
System Module
Handles system operations and application control
"""

import subprocess
import platform
import os
import psutil
from utils.logger import setup_logger

logger = setup_logger(__name__)

def open_application(app_name):
    """
    Open an application by name
    
    Args:
        app_name (str): Application name or path
    
    Returns:
        str: Result message
    """
    try:
        logger.info(f"Opening application: {app_name}")
        app_name = app_name.lower().strip()
        
        system = platform.system()
        
        if system == 'Windows':
            # Windows application names
            app_map = {
                'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                'firefox': 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'word': 'WINWORD.EXE',
                'excel': 'EXCEL.EXE',
                'powershell': 'powershell.exe',
                'cmd': 'cmd.exe'
            }
            
            app_path = app_map.get(app_name, app_name)
            subprocess.Popen(app_path)
            
        elif system == 'Darwin':  # macOS
            subprocess.Popen(['open', '-a', app_name])
            
        elif system == 'Linux':
            subprocess.Popen([app_name])
        
        logger.info(f"Successfully opened {app_name}")
        return f"Opening {app_name}"
    
    except Exception as e:
        logger.error(f"Error opening application: {str(e)}")
        return f"I couldn't open {app_name}"

def close_application(app_name):
    """
    Close an application by name
    
    Args:
        app_name (str): Application name
    
    Returns:
        str: Result message
    """
    try:
        logger.info(f"Closing application: {app_name}")
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    logger.info(f"Closed {app_name}")
                    return f"Closed {app_name}"
            except:
                pass
        
        return f"Could not find {app_name} running"
    
    except Exception as e:
        logger.error(f"Error closing application: {str(e)}")
        return "I couldn't close that application"

def get_system_info():
    """
    Get system information
    
    Returns:
        dict: System information
    """
    try:
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'ram_gb': psutil.virtual_memory().total / (1024**3),
            'available_ram_gb': psutil.virtual_memory().available / (1024**3)
        }
        logger.info(f"Retrieved system info: {info}")
        return info
    
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return {}

def lock_screen():
    """Lock the computer screen"""
    try:
        system = platform.system()
        logger.info("Locking screen")
        
        if system == 'Windows':
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        elif system == 'Darwin':
            subprocess.run(['open', '-a', 'Keychain Access', '--args', '-l'])
        elif system == 'Linux':
            subprocess.run(['loginctl', 'lock-session'])
        
        return "Screen locked"
    
    except Exception as e:
        logger.error(f"Error locking screen: {str(e)}")
        return "I couldn't lock the screen"

def shutdown_system():
    """Shutdown the computer"""
    try:
        logger.info("Initiating system shutdown")
        system = platform.system()
        
        if system == 'Windows':
            subprocess.run(['shutdown', '/s', '/t', '60'])
        elif system in ['Darwin', 'Linux']:
            subprocess.run(['shutdown', '-h', '+1'])
        
        return "System shutdown initiated"
    
    except Exception as e:
        logger.error(f"Error shutting down: {str(e)}")
        return "I couldn't shutdown the system"

def restart_system():
    """Restart the computer"""
    try:
        logger.info("Initiating system restart")
        system = platform.system()
        
        if system == 'Windows':
            subprocess.run(['shutdown', '/r', '/t', '60'])
        elif system in ['Darwin', 'Linux']:
            subprocess.run(['shutdown', '-r', '+1'])
        
        return "System restart initiated"
    
    except Exception as e:
        logger.error(f"Error restarting: {str(e)}")
        return "I couldn't restart the system"
