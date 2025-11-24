# TeraBox Telegram Bot

## Overview
TeraBox Telegram Bot is a Python-based Telegram bot that downloads and processes files from TeraBox links. The bot uses Pyrogram to interact with the Telegram API and includes a Flask health check server.

**Current State**: Fully featured production bot with premium system, auto-upload channels, and auto-delete functionality.

## Recent Changes
- **2025-11-24**: Videos sent in video format with thumbnail support
  - **Format**: Both primary and secondary upload functions use `send_video` format
  - **Streaming**: Supports streaming with `supports_streaming=True` for better UX
  - **Thumbnails**: Auto-generated thumbnails for video preview
  - **Duration**: Displays video duration when sending
  - **Applies to**: All video downloads (primary TeraBox API and secondary iTeraPlay API)

- **2025-11-24**: Fixed video filename extraction from TeraBox HTML
  - **Improvement**: Extracts actual filenames from TeraBox page instead of API generic "video.mp4"
  - **HTML Cleaning**: Decodes HTML entities and removes TeraBox branding from page titles
  - **Example**: `Cute_GirlBy_@Desipremier_On_Telegram.mp4` (clean, without page branding)
  - **Patterns**: Checks share_title, JSON name/title fields, data attributes in order

- **2025-11-24**: Fixed video filename corruption - disabled auto-rename by default
  - **Root Cause**: Auto-rename was enabled by default and applying "timestamp" pattern, causing filename corruption
  - **Fix**: Disabled auto-rename by default (changed default from "timestamp" to "" in config.py and database.py)
  - **Sanitization Improvement**: Changed from whitelist (only allow safe chars) to blacklist (remove only dangerous chars)
  - **Result**: Videos now save with their clean original filenames (e.g., "telegram @Desipremier SEDTPG.mp4")
  - Applied consistent sanitization to both primary and secondary download functions
  - Added debug logging to trace filename handling: `[DOWNLOAD]` and `[PRIMARY DOWNLOAD]` log entries
  - Users can now explicitly enable rename via `/rename on` or `/set_rename <pattern>` if desired

- **2025-11-24**: Simplified rename variables - removed {original_name}, made {file_name} primary
  - Removed {original_name} and {ext} variables for simplicity
  - Made {file_name} represent the complete original filename (with extension)
  - Reduced from 11 to 9 total variables, cleaner and easier to use
  - Updated /rename help text with simplified variable list:
    * File info: {file_name} (complete original filename), {file_size}
    * Date & time: {date}, {timestamp}, {datetime}, {time}
    * User info: {user_id}, {username}
  - Updated rename.py logic to handle filename with extension directly
  - API still prefers 'filename' field over 'server_filename' (cleaner extraction)

- **2025-11-24**: Secondary API with HLS streaming support
  - Implemented iTeraPlay secondary API as fallback for TeraBox downloads
  - HLS stream support via ffmpeg for videos not accessible via primary API
  - Progress tracking for HLS with "unknown total" UI (Option A):
    * Shows current download size and speed
    * No percentage bar for HLS (technical limitation of ffmpeg + HLS)
    * Clean, honest UI without misleading progress estimates
  - Auto-rename functionality working with secondary API (matches primary)
  - Metadata extraction (video title) from iTeraPlay API response
  - Bot seamlessly uses secondary API when primary fails

- **2025-11-22**: Complete feature implementation
  - Auto-upload channel system for premium users (command: `/set_upload_channel`, `/remove_upload_channel`)
  - Auto-delete downloaded files feature (toggle: `/toggle_autodelete`)
  - Admin settings panel with auto-delete toggle in admin menu
  - Premium QR code image added to upgrade page
  - All admin callbacks properly wired in admin panel
  - Fixed command exclusions in main download handler
  - Bot running successfully with all features active

## Project Architecture

### Core Components
- **bot.py**: Initializes the Pyrogram client and registers all handlers
- **main.py**: Entry point that starts both the Flask health server (port 8000) and the Pyrogram bot
- **config.py**: Configuration management using environment variables and constants
- **health.py**: Flask-based health check endpoint

### Directory Structure
```
├── core/               # Core bot logic
│   ├── responses.py    # Response handlers
│   └── router.py       # Handler registration
├── handlers/           # Command and message handlers
│   ├── download_handler.py
│   ├── premium.py
│   ├── admin.py
│   └── start.py
├── plugins/            # Plugin modules
│   ├── buttons.py      # All keyboard buttons centralized
│   ├── command.py      # Command handlers
│   ├── error_channel.py
│   ├── log_channel.py
│   ├── premium.py      # Premium manager class
│   ├── premium_upload.py  # Premium auto-upload
│   ├── storage_channel.py
│   └── script.py       # All UI text centralized
├── Theinertbotz/       # Core bot functionality
│   ├── api.py          # API integrations
│   ├── database.py     # MongoDB database operations
│   ├── download.py     # Download logic
│   ├── engine.py       # Core processing engine with auto-delete
│   ├── processing.py   # File processing
│   ├── thumbnail.py    # Thumbnail generation
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
- Collections: users, logs, settings

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
- `AUTO_DELETE`: Auto-delete downloaded files (default: "True")
- `PREMIUM_UPLOAD_CHANNEL`: Channel ID for premium user auto-uploads (optional)

## Features

### Premium System
- **Time-based Premium**: `/addpremium [user_id] [days]` for temporary, permanent if no days specified
- **Automatic Expiry**: Premium automatically downgraded when expiry date passes
- **Premium Upload Channel**: Auto-upload files from premium users to designated channel
- **Per-user Upload Channels**: Can be set dynamically via `/set_upload_channel` (stored in MongoDB)
- **Daily Download Limits**: Free users limited to 5 downloads/day, premium unlimited
- **Admin Status Check**: `/checkuser [user_id]` to view user tier and download stats

### Download & Processing
- **Direct Link Extraction**: Advanced HTML parsing for TeraBox links
- **Video Thumbnails**: Auto-generated for videos in storage and premium channels
- **File Renaming**: Auto-rename with variables ({file_name}, {timestamp}, {date}, etc.)
- **Progress Tracking**: Real-time download/upload progress with visual feedback
- **Error Logging**: Comprehensive error logging to ERROR_CHANNEL

### Auto-Delete Feature
- **Configurable**: Toggle on/off via admin panel or `/toggle_autodelete` command
- **Persistent**: Setting stored in MongoDB, survives bot restarts
- **Automatic Cleanup**: Deletes downloaded files after successful upload to user
- **Storage Optimization**: Helps manage disk space on server

### Admin Panel
- **Centralized Management**: `/admin` command opens full admin panel
- **Premium User Management**: Add/remove premium users with flexible durations
- **User Status Checking**: View individual user tier and daily download counts
- **Channel Configuration**: Set/remove premium upload channel dynamically
- **Settings Control**: Toggle auto-delete feature from admin menu
- **Full Button Navigation**: All features accessible via inline buttons with back buttons

### Channels
1. **LOG_CHANNEL**: Activity logging (successful downloads)
2. **ERROR_CHANNEL**: Error reporting (failed operations, API errors)
3. **STORAGE_CHANNEL**: File backup (all downloads as video/document with metadata)
4. **PREMIUM_UPLOAD_CHANNEL**: Auto-forward premium user downloads (set per-user via command)

### UI Design
- **Centralized Text**: All user-facing text in script.py for easy maintenance
- **Organized Buttons**: All keyboard buttons in plugins/buttons.py
- **Responsive Layout**: Back buttons throughout for easy navigation
- **Status Messages**: Clear feedback for all user actions

## Workflow
The bot runs via a single workflow:
- **Name**: Run TeraBox Bot
- **Command**: `python main.py`
- **Port**: 8000 (health check server)
- **Output**: Console

## Admin Commands
- `/admin` - Open admin panel
- `/addpremium [user_id] [days]` - Add premium user (days optional for permanent)
- `/removepremium [user_id]` - Remove premium from user
- `/checkuser [user_id]` - Check user status and download count
- `/set_upload_channel [channel_id]` - Set premium auto-upload channel
- `/remove_upload_channel` - Remove premium upload channel
- `/toggle_autodelete` - Toggle auto-delete feature on/off
- `/checkchannels` - Verify bot access to all configured channels

## User Commands
- `/start` - Welcome message
- `/help` - Command list
- `/premium` - Premium info and upgrade
- `/rename` - Auto-rename settings

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
- QR code image URL stored as public constant (no sensitive data)

### Premium QR Code
- URL: `https://i.ibb.co/hFjZ6CWD/photo-2025-08-10-02-24-51-7536777335068950548.jpg`
- Displayed in premium upgrade screen
- Shows pricing: $4.99/month, $39.99/year (33% savings)
- Includes contact info: DM @Theinertbotz

## User Preferences
- Premium tier system with flexible time-based expiration
- Auto-upload channel for premium files
- Auto-delete files to manage storage
- Centralized admin controls

