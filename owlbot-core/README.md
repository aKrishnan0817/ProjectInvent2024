# Owlbot Core

A modular and organized implementation of the Owlbot therapy assistant.

## Project Structure

```
owlbot-core/
├── core/           # Core functionality
│   └── owlbot.py   # Main Owlbot agent implementation
├── modes/          # Different interaction modes
│   ├── base.py     # Base mode class
│   ├── distress.py # Distress mode
│   ├── game.py     # Game mode
│   └── ...
├── tools/          # Tool implementations
├── utils/          # Utility functions
├── config/         # Configuration files
│   └── sensitive_data.py
└── main.py         # Entry point
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run the bot:
```bash
python main.py
```

## Configuration

All sensitive data and configuration is stored in environment variables:
- `OWLBOT_EMAIL`: Email address for notifications
- `OWLBOT_EMAIL_PASSWORD`: Email password
- `OWLBOT_GUARDIAN_EMAIL`: Guardian's email for notifications
- `OPENAI_API_KEY`: OpenAI API key

## Modes

The bot supports several interaction modes:
- Distress Mode: Handles emergency situations
- Game Mode: Interactive games
- Story Mode: Storytelling
- Psychoeducation Mode: Educational content
- Coping Mode: Coping skills training

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 