"""
Smart Home Module
Handles IoT and smart device control
"""

from utils.logger import setup_logger

logger = setup_logger(__name__)

class SmartDevice:
    """Base class for smart devices"""
    
    def __init__(self, name, device_type):
        """Initialize smart device"""
        self.name = name
        self.device_type = device_type
        self.state = 'off'
        self.brightness = 100
        logger.info(f"Smart device initialized: {name} ({device_type})")
    
    def turn_on(self):
        """Turn on device"""
        self.state = 'on'
        logger.info(f"Turned on {self.name}")
        return f"{self.name} is now on"
    
    def turn_off(self):
        """Turn off device"""
        self.state = 'off'
        logger.info(f"Turned off {self.name}")
        return f"{self.name} is now off"
    
    def get_state(self):
        """Get device state"""
        return f"{self.name} is {self.state}"

class SmartLight(SmartDevice):
    """Smart light device"""
    
    def __init__(self, name):
        super().__init__(name, 'light')
        self.color = 'white'
    
    def set_brightness(self, level):
        """Set brightness level"""
        if 0 <= level <= 100:
            self.brightness = level
            logger.info(f"Set {self.name} brightness to {level}%")
            return f"Set {self.name} brightness to {level}%"
        return "Brightness must be between 0 and 100"
    
    def set_color(self, color):
        """Set light color"""
        self.color = color
        logger.info(f"Set {self.name} color to {color}")
        return f"Set {self.name} color to {color}"

class SmartThermostat(SmartDevice):
    """Smart thermostat"""
    
    def __init__(self, name):
        super().__init__(name, 'thermostat')
        self.temperature = 72  # Fahrenheit
        self.mode = 'auto'  # heat, cool, auto
    
    def set_temperature(self, temp):
        """Set target temperature"""
        self.temperature = temp
        logger.info(f"Set {self.name} to {temp}°F")
        return f"Set temperature to {temp}°F"
    
    def set_mode(self, mode):
        """Set heating/cooling mode"""
        valid_modes = ['heat', 'cool', 'auto']
        if mode.lower() in valid_modes:
            self.mode = mode.lower()
            logger.info(f"Set {self.name} mode to {mode}")
            return f"Set mode to {mode}"
        return f"Invalid mode. Choose from: {', '.join(valid_modes)}"
    
    def get_status(self):
        """Get thermostat status"""
        return f"Temperature: {self.temperature}°F, Mode: {self.mode}"

class SmartHome:
    """Smart home controller"""
    
    def __init__(self):
        """Initialize smart home"""
        self.devices = {}
        logger.info("Smart Home initialized")
    
    def add_device(self, device):
        """Add a smart device"""
        self.devices[device.name.lower()] = device
        logger.info(f"Added device: {device.name}")
    
    def control_device(self, device_name, action, parameter=None):
        """
        Control a smart device
        
        Args:
            device_name (str): Name of device
            action (str): Action to perform
            parameter (str): Optional parameter
        
        Returns:
            str: Result message
        """
        try:
            device = self.devices.get(device_name.lower())
            if not device:
                return f"Device {device_name} not found"
            
            if action.lower() == 'on':
                return device.turn_on()
            elif action.lower() == 'off':
                return device.turn_off()
            elif action.lower() == 'brightness' and isinstance(device, SmartLight):
                return device.set_brightness(int(parameter))
            elif action.lower() == 'color' and isinstance(device, SmartLight):
                return device.set_color(parameter)
            elif action.lower() == 'temperature' and isinstance(device, SmartThermostat):
                return device.set_temperature(int(parameter))
            elif action.lower() == 'mode' and isinstance(device, SmartThermostat):
                return device.set_mode(parameter)
            else:
                return f"Unknown action: {action}"
        
        except Exception as e:
            logger.error(f"Error controlling device: {str(e)}")
            return "I couldn't control that device"
    
    def list_devices(self):
        """List all smart devices"""
        if not self.devices:
            return "No devices configured"
        
        devices_str = "Smart devices: " + ", ".join(self.devices.keys())
        logger.info(devices_str)
        return devices_str
    
    def get_device_status(self, device_name):
        """Get status of a device"""
        device = self.devices.get(device_name.lower())
        if device:
            return device.get_state()
        return f"Device {device_name} not found"

# Example usage and initialization
def init_smart_home():
    """Initialize example smart home setup"""
    home = SmartHome()
    
    # Add some example devices
    living_room_light = SmartLight("Living Room Light")
    bedroom_light = SmartLight("Bedroom Light")
    thermostat = SmartThermostat("Thermostat")
    
    home.add_device(living_room_light)
    home.add_device(bedroom_light)
    home.add_device(thermostat)
    
    logger.info("Example smart home initialized with 3 devices")
    return home
