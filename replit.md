# TeraBox Telegram Bot

## Overview
TeraBox Telegram Bot is a Python-based Telegram bot that downloads and processes files from TeraBox links. The bot uses Pyrogram to interact with the Telegram API and includes a Flask health check server.

**Current State**: Successfully configured and running in Replit environment.

## Recent Changes
- **2025-11-22**: Initial setup and bug fixes
  - Installed Python 3.11 and all required dependencies
  - Removed hardcoded credentials from config.py for security
  - Configured environment variables and secrets
  - Set up workflow to run the bot with health check server on port 8000
  - Created .gitignore for Python project
  - **Bug Fixes**:
    - Fixed parse_mode errors: Changed all instances from string "html" to proper Pyrogram enum `enums.ParseMode.HTML`
    - Fixed type hints in processing.py (human_size function now accepts int, float, or None)
    - Fixed edit_coro signature in uploader.py to use proper parse_mode enum
  - Bot is now running successfully and error-free

## Project Architecture

### Core Components
- **bot.py**: Initializes the Pyrogram client and registers all handlers
- **main.py**: Entry point that starts both the Flask health server (port 8000) and the Pyrogram bot
- **config.py**: Configuration management using environment variables
- **health.py**: Flask-based health check endpoint

### Directory Structure
```
├── core/               # Core bot logic
│   ├── responses.py    # Response handlers
│   └── router.py       # Handler registration
├── handlers/           # Command and message handlers
│   ├── download_handler.py
│   └── start.py
├── plugins/            # Plugin modules
│   ├── error_channel.py
│   ├── log_channel.py
│   └── storage_channel.py
├── Theinertbotz/       # Core bot functionality
│   ├── api.py          # API integrations
│   ├── database.py     # MongoDB database operations
│   ├── download.py     # Download logic
│   ├── engine.py       # Core processing engine
│   ├── processing.py   # File processing
│   ├── uploader.py     # Upload functionality
│   └── utils.py        # Utility functions
├── sessions/           # Pyrogram session files (auto-generated)
├── downloads/          # Temporary download directory
└── requirements.txt    # Python dependencies
```

### Technologies
- **Python 3.11**: Main programming language
- **Pyrogram 2.0.106**: Telegram MTProto API framework
- **Flask**: Health check HTTP server
- **MongoDB**: Database for storing bot data
- **aiohttp**: Async HTTP client

### Database
- MongoDB (external connection via MONGO_URI secret)
- Database name: teraboxbot

### API Integration
- TeraBox API endpoint: `https://teraapi.boogafantastic.workers.dev/play?url={url}`

## Environment Configuration

### Required Secrets (encrypted)
These are stored as Replit Secrets and are required for the bot to function:
- `BOT_TOKEN`: Telegram bot token from @BotFather
- `API_HASH`: Telegram API hash from https://my.telegram.org
- `MONGO_URI`: MongoDB connection string

### Required Environment Variables
These are stored as shared environment variables:
- `API_ID`: Telegram API ID (numeric)
- `LOG_CHANNEL`: Telegram channel ID for logs (numeric, format: -1001234567890)
- `ERROR_CHANNEL`: Telegram channel ID for errors (numeric)
- `STORAGE_CHANNEL`: Telegram channel ID for file storage (numeric)

### Optional Environment Variables
These have default values and can be customized:
- `MONGO_DB`: MongoDB database name (default: "teraboxbot")
- `DOWNLOAD_DIR`: Download directory path (default: "downloads")
- `WORKERS`: Number of worker threads (default: 20)

## Workflow
The bot runs via a single workflow:
- **Name**: Run TeraBox Bot
- **Command**: `python main.py`
- **Port**: 8000 (health check server)
- **Output**: Console

## Development Notes

### Running Locally
The workflow automatically starts the bot when you run the Repl. The bot includes:
1. Flask health server on port 8000 (background thread)
2. Pyrogram Telegram bot (main thread)

### Health Check
Access the health endpoint at `http://0.0.0.0:8000/` to verify the service is running. Returns:
```json
{"status": "ok", "service": "TeraBoxBot"}
```

### Session Files
Pyrogram creates session files in the `sessions/` directory. These are auto-generated and should not be committed to version control (already in .gitignore).

### Security
- All sensitive credentials are stored as Replit Secrets or environment variables
- No hardcoded credentials in the codebase
- Session files and downloads are excluded from git

## User Preferences
None set yet.
