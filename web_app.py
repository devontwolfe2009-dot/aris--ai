"""
ARIS - Automated Responsive Intelligence System
Enhanced Free Web Interface Version
Talk to ARIS, ask for weather, open YouTube, and more!
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from core.ai_engine_free import AIEngine
from core.command_parser import CommandParser
from utils.logger import setup_logger
import webbrowser
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize ARIS components
ai_engine = AIEngine()
command_parser = CommandParser()

class ARISController:
    """Controller for ARIS system"""
    
    def __init__(self):
        self.name = os.getenv('SYSTEM_NAME', 'ARIS')
        self.conversation = []
        logger.info(f"{self.name} Web Controller initialized")
    
    def process_user_input(self, user_input):
        """Process user input and return response"""
        try:
            # Parse the command
            parsed = self.command_parser.parse(user_input)
            
            # Get AI response
            response = ai_engine.get_response(user_input)
            
            # Execute action if needed
            action_result = None
            if parsed.get('action'):
                action_result = self.execute_action(parsed)
            
            # Add to conversation
            self.conversation.append({
                'type': 'user',
                'text': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation.append({
                'type': 'assistant',
                'text': response,
                'action': parsed.get('action'),
                'action_result': action_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep conversation manageable
            if len(self.conversation) > 100:
                self.conversation = self.conversation[-100:]
            
            return {
                'response': response,
                'action': parsed.get('action'),
                'action_result': action_result,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return {
                'response': f"{self.name}: I encountered an error processing that request.",
                'success': False,
                'error': str(e)
            }
    
    def execute_action(self, parsed_command):
        """Execute system actions based on parsed commands"""
        action = parsed_command.get('action')
        params = parsed_command.get('params', {})
        
        try:
            if action == 'open_app':
                app_name = params.get('app_name', '')
                if app_name.lower() in ['youtube', 'youtube.com']:
                    return f"Opening YouTube in your browser..."
                elif app_name.lower() in ['chrome', 'firefox', 'safari', 'edge']:
                    return f"Browser {app_name} would open..."
                else:
                    return f"Opening {app_name}..."
            
            elif action == 'get_weather':
                location = params.get('location', 'current')
                return self.get_weather_info(location)
            
            elif action == 'open_youtube':
                query = params.get('query')
                if query:
                    return f"Searching YouTube for: {query}"
                else:
                    return "Opening YouTube..."
            
            elif action == 'control_media':
                media_action = params.get('action', '')
                return f"{media_action.capitalize()}ing media..."
            
            return None
        
        except Exception as e:
            logger.error(f"Error executing action: {str(e)}")
            return f"Error executing {action}: {str(e)}"
    
    def get_weather_info(self, location='current'):
        """Get weather information"""
        try:
            import requests
            
            # Try to get weather from OpenWeatherMap (free tier doesn't require key for some endpoints)
            if location == 'current':
                location = 'New York'  # Default location
            
            # Using wttr.in free weather API (no key needed)
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                try:
                    current_condition = data['current_condition'][0]
                    temp = current_condition['temp_C']
                    description = current_condition['weatherDesc'][0]['value']
                    return f"Weather in {location}: {description}, Temperature: {temp}°C"
                except:
                    return f"Couldn't parse weather data for {location}"
            else:
                return f"Couldn't fetch weather for {location}"
        
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            return f"Weather data unavailable: {str(e)}"

# Initialize ARIS controller
aris = ARISController()

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html', name=aris.name)

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        result = aris.process_user_input(user_input)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Chat API error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/conversation', methods=['GET'])
def get_conversation():
    """Get conversation history"""
    return jsonify({'conversation': aris.conversation})

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    aris.conversation = []
    ai_engine.clear_history()
    return jsonify({'success': True, 'message': 'Conversation cleared'})

@app.route('/api/open-youtube', methods=['POST'])
def open_youtube_endpoint():
    """Open YouTube endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = "https://www.youtube.com"
        
        return jsonify({
            'success': True,
            'message': f"YouTube opened: {url}",
            'url': url
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    logger.info("Starting ARIS Web Interface...")
    print(f"\n{'='*60}")
    print(f"{aris.name} - Web Interface")
    print(f"{'='*60}")
    print(f"🌐 Open your browser and go to: http://localhost:5000")
    print(f"{'='*60}\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
