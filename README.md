# ARIS - Automated Responsive Intelligence System

ARIS is a voice-activated AI assistant system similar to Jarvis from Iron Man. It can perform a wide variety of tasks including opening applications, controlling smart devices, fetching weather information, making calls, and more.

## Features

- 🎙️ **Voice Recognition** - Listen and respond to voice commands
- 🌐 **Web Integration** - Open YouTube, browse websites, fetch weather data
- 📞 **Communication** - Make calls and send messages
- 🎵 **Media Control** - Control music playback and volume
- 🔧 **System Control** - Open applications and manage system functions
- 🧠 **AI Powered** - Powered by OpenAI API for intelligent responses
- 🔌 **Extensible** - Easy to add new capabilities and integrations

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Required API keys for third-party services (optional)

### Installation

```bash
git clone https://github.com/devontwolfe2009-dot/aris--ai.git
cd aris--ai
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the root directory
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Running ARIS

```bash
python main.py
```

## Architecture

```
aris--ai/
├── main.py                 # Entry point
├── core/
│   ├── ai_engine.py       # OpenAI integration
│   ├── voice_handler.py   # Voice recognition & output
│   └── command_parser.py  # Parse and route commands
├── modules/
│   ├── web_module.py      # Web browsing, weather, YouTube
│   ├── media_module.py    # Music and media control
│   ├── communication.py   # Calls and messaging
│   ├── system_module.py   # System and app control
│   └── smart_home.py      # IoT and smart device control
├── utils/
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging utilities
└── requirements.txt       # Python dependencies
```

## Usage Examples

### Voice Commands

- "ARIS, open YouTube"
- "What's the weather like?"
- "Tell me a joke"
- "Open Spotify"
- "Make a call to John"
- "What's the news?"
- "Set a reminder for 3 PM"

## API Integration

ARIS uses the following APIs:

- **OpenAI GPT-4** - For conversational AI and command understanding
- **Weather API** - For weather information
- **YouTube/Web APIs** - For web content access
- **System APIs** - For OS-level automation

## Contributing

Feel free to contribute by:

1. Forking the repository
2. Creating a feature branch
3. Committing your changes
4. Pushing to the branch
5. Creating a Pull Request

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is for educational purposes. Ensure you comply with all applicable laws and terms of service when using third-party APIs.