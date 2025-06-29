import os
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.json file
    """
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info("Configuration loaded successfully")
        return config
        
    except FileNotFoundError:
        logger.warning("config.json not found, using default configuration")
        return get_default_config()
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing config.json: {e}")
        return get_default_config()
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration values
    """
    return {
        "bot_name": "Homeland RP | Official Bot",
        "command_prefix": "!",
        "roblox_servers": [
            "https://www.roblox.com/games/1234567890/Homeland-RP?privateServerLinkCode=example1",
            "https://www.roblox.com/games/1234567890/Homeland-RP?privateServerLinkCode=example2"
        ],
        "admin_roles": [
            "Admin",
            "Administrator",
            "Owner",
            "Server Owner"
        ],
        "moderator_roles": [
            "Moderator",
            "Mod",
            "Staff",
            "Helper"
        ],
        "protected_roles": [
            "Admin",
            "Administrator",
            "Owner",
            "Server Owner",
            "Bot",
            "@everyone"
        ],
        "role_categories": {
            "Staff Roles": [
                "Admin",
                "Moderator",
                "Helper",
                "Staff"
            ],
            "RP Roles": [
                "Police",
                "Civilian",
                "Criminal",
                "EMS",
                "Fire Department",
                "Government"
            ],
            "Special Roles": [
                "VIP",
                "Donator",
                "Nitro Booster",
                "Verified"
            ]
        },
        "owner_ids": [
            # Add Discord user IDs of bot owners here
            # Example: 123456789012345678
        ],
        "logging": {
            "level": "INFO",
            "file": "homeland_bot.log",
            "max_size": 10485760,  # 10MB
            "backup_count": 5
        }
    }

def save_config(config: Dict[str, Any]) -> bool:
    """
    Save configuration to config.json file
    """
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        logger.info("Configuration saved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False

def get_environment_config() -> Dict[str, Any]:
    """
    Get configuration from environment variables
    """
    env_config = {}
    
    # Bot token
    if os.getenv('DISCORD_BOT_TOKEN'):
        env_config['bot_token'] = os.getenv('DISCORD_BOT_TOKEN')
    
    # Owner IDs from environment
    owner_ids_str = os.getenv('BOT_OWNER_IDS', '')
    if owner_ids_str:
        try:
            env_config['owner_ids'] = [int(id.strip()) for id in owner_ids_str.split(',') if id.strip()]
        except ValueError:
            logger.warning("Invalid BOT_OWNER_IDS format in environment variables")
    
    # Roblox server links from environment
    server_links_str = os.getenv('ROBLOX_SERVER_LINKS', '')
    if server_links_str:
        env_config['roblox_servers'] = [link.strip() for link in server_links_str.split(',') if link.strip()]
    
    # Logging level
    log_level = os.getenv('LOG_LEVEL', '').upper()
    if log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        if 'logging' not in env_config:
            env_config['logging'] = {}
        env_config['logging']['level'] = log_level
    
    return env_config

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged

# Load and merge configurations
BOT_CONFIG = load_config()
ENV_CONFIG = get_environment_config()
BOT_CONFIG = merge_configs(BOT_CONFIG, ENV_CONFIG)

# Validate critical configuration
if not BOT_CONFIG.get('roblox_servers'):
    logger.warning("No Roblox server links configured!")

if not BOT_CONFIG.get('owner_ids'):
    logger.warning("No bot owner IDs configured!")

logger.info(f"Bot configuration loaded: {BOT_CONFIG['bot_name']}")
