# TeraBox Telegram Bot

## Overview
The TeraBox Telegram Bot is a Python-based solution designed to download and process files from TeraBox links. It leverages the Telegram API via Pyrogram and incorporates a Flask-based health check server. The bot offers sequential bulk link processing, a premium user system, auto-upload capabilities to designated channels, and an auto-delete function for downloaded files. Its primary purpose is to provide a seamless and efficient way for users to handle TeraBox downloads directly through Telegram.

## User Preferences
- Premium tier system with flexible time-based expiration
- Auto-upload channel for premium files
- Auto-delete files to manage storage
- Centralized admin controls

## System Architecture

### Core Components and Design
The bot's architecture is modular, separating core logic, handlers, and plugin functionalities.
- **`bot.py`**: Initializes the Pyrogram client and registers all event handlers.
- **`main.py`**: The application entry point, initiating both the Flask health server and the Pyrogram bot.
- **`config.py`**: Handles configuration using environment variables.
- **`health.py`**: Provides a Flask endpoint for health checks.
- **Handlers**: Dedicated modules for managing commands (e.g., download, premium, admin, start).
- **Plugins**: Centralized modules for UI elements (buttons, scripts), logging, premium features, and storage channel management.
- **Theinertbotz**: Contains core functionalities such as API integrations, database operations, download logic, file processing, thumbnail generation, and file uploading.

### Directory Structure
The project is organized into `core/`, `handlers/`, `plugins/`, and `Theinertbotz/` directories to maintain separation of concerns.

### Technologies
- **Python 3.11**: Primary programming language.
- **Pyrogram 2.0.106**: Used for Telegram API interaction.
- **Flask**: For the health check HTTP server.
- **MongoDB**: The chosen database for persistent data storage.
- **aiohttp**: Asynchronous HTTP client.

### Database
- **MongoDB**: External connection via `MONGO_URI`.
- **Collections**: `users`, `logs`, `settings`.

### UI Design
- **Centralized Text**: All user-facing messages are managed in `script.py`.
- **Organized Buttons**: Keyboard buttons are defined in `plugins/buttons.py`.
- **Responsive Layout**: Features back buttons for intuitive navigation.
- **Status Messages**: Provides clear and continuous feedback for user actions and bot processes (e.g., download, upload, waiting).

### Features
- **Premium System**: Time-based premium with automatic expiry, premium upload channel, daily download limits, and admin status checks.
- **Download & Processing**: Advanced HTML parsing for TeraBox links, auto-generated video thumbnails, customizable file renaming with variables, real-time progress tracking, and comprehensive error logging.
- **Auto-Delete Feature**: Configurable and persistent setting to automatically delete downloaded files post-upload.
- **Admin Panel**: A centralized `/admin` command providing management capabilities for premium users, channel configuration, and bot settings.
- **Channels**: Dedicated channels for logging, error reporting, file storage, and premium user uploads.
- **Sequential Processing**: Guarantees one-by-one processing of bulk links with a 1-second delay between each.
- **Video Handling**: Sends videos in video format with thumbnail support, streaming, and improved filename extraction/sanitization.
- **Secondary API**: Implements iTeraPlay as a fallback for TeraBox downloads, supporting HLS streaming via ffmpeg.

## External Dependencies
- **Telegram API**: Accessed via the Pyrogram library.
- **TeraBox API**: Custom endpoint `https://teraapi.boogafantastic.workers.dev/play?url={url}` for link processing.
- **MongoDB**: External database for persistent storage.
- **iTeraPlay API**: Used as a secondary API for fallback downloads and HLS streaming.
- **ffmpeg**: Utilized for HLS streaming and video processing.