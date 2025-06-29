import logging
import logging.handlers
import os
from datetime import datetime
from config.settings import BOT_CONFIG

def setup_logger() -> logging.Logger:
    """
    Setup and configure the bot logger
    """
    # Get logging configuration
    log_config = BOT_CONFIG.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO').upper())
    log_file = log_config.get('file', 'homeland_bot.log')
    max_size = log_config.get('max_size', 10485760)  # 10MB
    backup_count = log_config.get('backup_count', 5)
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    date_format = log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
    
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file_path = os.path.join(logs_dir, log_file)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format, date_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging configured - Level: {log_config.get('level', 'INFO')}, File: {log_file_path}")
        
    except Exception as e:
        logger.error(f"Failed to setup file logging: {e}")
        logger.info("Continuing with console logging only")
    
    # Log startup information
    logger.info("=" * 50)
    logger.info("Homeland RP Bot Starting Up")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    
    return logger

class BotLogger:
    """
    Custom logger class for bot-specific logging
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_command_usage(self, user: str, command: str, guild: str = None):
        """Log command usage"""
        guild_info = f"in {guild}" if guild else "in DM"
        self.logger.info(f"Command '{command}' used by {user} {guild_info}")
    
    def log_role_change(self, target: str, role: str, action: str, moderator: str, guild: str):
        """Log role changes"""
        self.logger.info(f"Role {action}: '{role}' {action}{'d' if action.endswith('e') else 'ed'} {'to' if action == 'add' else 'from'} {target} by {moderator} in {guild}")
    
    def log_permission_denied(self, user: str, command: str, required_level: str):
        """Log permission denied attempts"""
        self.logger.warning(f"Permission denied: {user} attempted to use '{command}' (requires {required_level})")
    
    def log_error(self, error: str, context: str = None):
        """Log errors with context"""
        context_info = f" in {context}" if context else ""
        self.logger.error(f"Error{context_info}: {error}")
    
    def log_server_link_request(self, user: str, guild: str = None):
        """Log server link requests"""
        guild_info = f"in {guild}" if guild else "in DM"
        self.logger.info(f"Server link requested by {user} {guild_info}")

def get_bot_logger(name: str) -> BotLogger:
    """
    Get a bot-specific logger instance
    """
    return BotLogger(name)

# Create specific loggers for different components
command_logger = get_bot_logger('commands')
role_logger = get_bot_logger('roles')
permission_logger = get_bot_logger('permissions')
server_logger = get_bot_logger('server')
