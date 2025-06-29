# Homeland RP Discord Bot

## Overview

This is a Discord bot designed for the Homeland RP Roblox server community. The bot provides essential server management features including role management, server link distribution, and permission-based command access. Built with Python using the discord.py library, it follows a modular architecture with clear separation of concerns across different components.

## System Architecture

The bot follows a modular architecture pattern with the following key design principles:

1. **Separation of Concerns**: Each component has a specific responsibility (commands, permissions, role management, etc.)
2. **Configuration Management**: Centralized configuration system using JSON files with fallback defaults
3. **Permission-Based Access Control**: Hierarchical permission system with multiple access levels
4. **Logging**: Comprehensive logging system with file rotation and configurable levels
5. **Async-First Design**: Built around Discord.py's asynchronous architecture

## Key Components

### Core Bot (`main.py`)
- **HomelandBot Class**: Main bot instance extending `commands.Bot`
- **Setup Hook**: Handles command registration and slash command synchronization
- **Event Handlers**: Manages bot ready state and presence updates
- **Problem Addressed**: Need for a centralized bot instance with proper initialization
- **Solution**: Custom bot class with async setup hooks for proper command loading

### Command System (`bot/commands.py`)
- **Slash Commands**: Modern Discord slash command implementation
- **Server Link Distribution**: Provides Roblox private server links to users
- **Role Management Commands**: Admin/moderator tools for user role assignment
- **Problem Addressed**: Need for interactive Discord commands with permission controls
- **Solution**: Discord.py's application command system with custom permission decorators

### Permission Management (`bot/permissions.py`)
- **Permission Levels**: Four-tier system (USER, MODERATOR, ADMIN, OWNER)
- **Role-Based Access**: Permission checking based on Discord roles and permissions
- **Hierarchical Structure**: Clear escalation path from user to owner
- **Problem Addressed**: Need for granular access control across different user types
- **Solution**: Enum-based permission levels with role and user ID checking

### Role Management (`bot/role_manager.py`)
- **Safe Role Assignment**: Protected role system preventing unauthorized access
- **Hierarchy Validation**: Ensures bot can only assign roles within its permission scope
- **Audit Trail**: Logging of all role changes with moderator attribution
- **Problem Addressed**: Need for controlled role assignment while preventing privilege escalation
- **Solution**: Multi-layer validation system with protected role lists

### Server Management (`bot/server_manager.py`)
- **Link Rotation**: Distributes multiple server links to balance load
- **Error Handling**: Graceful fallback when server links are unavailable
- **Random Selection**: Optional random server link distribution
- **Problem Addressed**: Need to distribute Roblox server access across multiple private servers
- **Solution**: Simple rotation system with configurable server link pool

### Configuration System (`config/settings.py`)
- **JSON Configuration**: Human-readable configuration files
- **Default Fallbacks**: Automatic fallback to defaults if config is missing/invalid
- **Runtime Loading**: Configuration loaded at startup with error handling
- **Problem Addressed**: Need for flexible configuration without code changes
- **Solution**: JSON-based config with comprehensive error handling and defaults

### Logging System (`utils/logger.py`)
- **Rotating File Logs**: Automatic log rotation to prevent disk space issues
- **Configurable Levels**: Adjustable logging verbosity
- **Multiple Outputs**: Both console and file logging with proper formatting
- **Problem Addressed**: Need for comprehensive debugging and audit trails
- **Solution**: Python's logging module with rotating file handlers

## Data Flow

1. **Bot Initialization**: Configuration loading → Logger setup → Bot instance creation
2. **Command Processing**: User interaction → Permission validation → Command execution → Response
3. **Role Management**: Command received → Permission check → Role validation → Discord API call → Audit log
4. **Server Links**: Request received → Link selection → Embed creation → Response delivery

## External Dependencies

### Core Dependencies
- **discord.py**: Primary Discord API wrapper for bot functionality
- **asyncio**: Asynchronous programming support (Python standard library)
- **logging**: Comprehensive logging system (Python standard library)
- **json**: Configuration file parsing (Python standard library)
- **os**: File system operations (Python standard library)

### Discord API Integration
- **Application Commands**: Slash command system for modern Discord interactions
- **Guild Management**: Server-specific role and permission management
- **Embed Messages**: Rich message formatting for better user experience
- **Presence Management**: Bot status and activity display

## Deployment Strategy

### Environment Requirements
- **Python 3.8+**: Required for discord.py compatibility
- **Discord Bot Token**: Required environment variable for authentication
- **File System Access**: For configuration files and log storage

### Configuration Management
- **Environment Variables**: Bot token and sensitive configuration
- **JSON Files**: Non-sensitive configuration like role names and server links
- **Default Fallbacks**: Ensures bot runs even with missing configuration

### Logging and Monitoring
- **File-Based Logging**: Persistent log storage with automatic rotation
- **Console Output**: Real-time monitoring during development
- **Error Tracking**: Comprehensive exception logging for debugging

### Scalability Considerations
- **Single Guild Focus**: Designed for one primary Discord server
- **Memory Efficient**: Minimal state storage, relies on Discord API for data
- **Async Architecture**: Can handle multiple concurrent requests efficiently

## Changelog

```
Changelog:
- June 29, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```