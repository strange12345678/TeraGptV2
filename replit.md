# TeraBox Telegram Bot

## Overview
The TeraBox Telegram Bot is a Python-based Telegram bot designed to download and process files from TeraBox links. It uses Pyrogram for Telegram API interaction and includes a Flask health check server. The bot provides a comprehensive solution for managing TeraBox downloads, featuring a premium system, auto-upload capabilities, and efficient bulk link processing with sequential handling. The project aims to offer a user-friendly and reliable service for accessing and organizing content from TeraBox.

## User Preferences
- Premium tier system with flexible time-based expiration
- Auto-upload channel for premium files
- Auto-delete files to manage storage
- Centralized admin controls

## System Architecture

### Core Components
- **bot.py**: Initializes the Pyrogram client and registers all handlers.
- **main.py**: Entry point that starts both the Flask health server and the Pyrogram bot.
- **config.py**: Handles configuration using environment variables.
- **health.py**: Implements a Flask-based health check endpoint.

### Directory Structure
- `core/`: Contains core bot logic like response handlers and router.
- `handlers/`: Stores command and message handlers (e.g., download, premium, admin, start).
- `plugins/`: Houses modular components such as buttons, command handlers, and channel-specific logic (error, log, premium_upload, storage).
- `Theinertbotz/`: Encapsulates core bot functionalities including API integrations, database operations, download logic, processing, thumbnail generation, uploader, and utility functions.
- `sessions/`: Stores Pyrogram session files.
- `downloads/`: Temporary directory for downloaded files.

### Technologies
- **Python 3.11**
- **Pyrogram 2.0.106**
- **Flask**
- **MongoDB**
- **aiohttp**

### UI Design
- **Centralized Text**: All user-facing text is managed in `script.py`.
- **Organized Buttons**: Keyboard buttons are defined in `plugins/buttons.py`.
- **Responsive Layout**: Includes back buttons for navigation.
- **Status Messages**: Provides clear feedback for user actions and bot operations.

## External Dependencies

### Database
- **MongoDB**: Used for storing bot data (users, logs, settings), connected via `MONGO_URI`.

### API Integration
- **TeraBox API**: Utilized for direct link extraction and file access.
- **iTeraPlay API**: Secondary API providing fallback for TeraBox downloads, including HLS streaming support.

### Environment Configuration
- **Required Secrets**: `BOT_TOKEN`, `API_HASH`, `MONGO_URI`.
- **Required Environment Variables**: `API_ID`, `LOG_CHANNEL`, `ERROR_CHANNEL`, `STORAGE_CHANNEL`.
- **Optional Environment Variables**: `MONGO_DB`, `DOWNLOAD_DIR`, `WORKERS`, `AUTO_DELETE`, `PREMIUM_UPLOAD_CHANNEL`.

## Recent Changes (Nov 2025)

### Channel Forwarding Fix
- **Issue**: "Peer id invalid" errors prevented files from being forwarded to configured channels
- **Root Cause**: Pyrogram requires channel peers to be resolved before sending messages, especially with fresh sessions
- **Solution**: Added `get_chat()` peer resolution in all channel plugins before any send operations:
  - `plugins/storage_channel.py` - Resolves peer before backing up files
  - `plugins/log_channel.py` - Resolves peer before sending logs  
  - `plugins/error_channel.py` - Resolves peer before sending errors
  - `plugins/premium_upload.py` - Resolves peer before premium uploads
- **Startup Hook**: `main.py` now resolves all configured channels on first message, surfacing configuration issues early

### Channel Requirements
- Bot must be added as **ADMIN** to all configured channels
- Channel IDs must be negative numbers (e.g., `-1001234567890`)
- Get correct channel IDs by forwarding a message from the channel to @RawDataBot