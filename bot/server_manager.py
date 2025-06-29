import asyncio
import logging
import random
from typing import Optional
from config.settings import BOT_CONFIG

logger = logging.getLogger(__name__)

class ServerManager:
    def __init__(self):
        self.server_links = BOT_CONFIG['roblox_servers']
        self.current_link_index = 0
    
    async def get_server_link(self) -> str:
        """
        Get a Roblox private server link
        Returns the server link or raises an exception if none available
        """
        try:
            if not self.server_links:
                raise Exception("No server links configured")
            
            # For now, return a rotating server link
            # In a real implementation, you might want to check server status
            link = self.server_links[self.current_link_index % len(self.server_links)]
            self.current_link_index += 1
            
            logger.info(f"Provided server link: {link[:50]}...")  # Log partial link for security
            return link
            
        except Exception as e:
            logger.error(f"Error getting server link: {e}")
            raise Exception("Unable to retrieve server link")
    
    async def get_random_server_link(self) -> str:
        """
        Get a random server link from available servers
        """
        try:
            if not self.server_links:
                raise Exception("No server links configured")
            
            link = random.choice(self.server_links)
            logger.info(f"Provided random server link: {link[:50]}...")
            return link
            
        except Exception as e:
            logger.error(f"Error getting random server link: {e}")
            raise Exception("Unable to retrieve server link")
    
    async def add_server_link(self, link: str, admin_user: str) -> bool:
        """
        Add a new server link (for future implementation with persistent storage)
        """
        try:
            if link not in self.server_links:
                self.server_links.append(link)
                logger.info(f"New server link added by {admin_user}")
                return True
            else:
                logger.warning(f"Duplicate server link attempted to be added by {admin_user}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding server link: {e}")
            return False
    
    async def remove_server_link(self, link: str, admin_user: str) -> bool:
        """
        Remove a server link (for future implementation with persistent storage)
        """
        try:
            if link in self.server_links:
                self.server_links.remove(link)
                logger.info(f"Server link removed by {admin_user}")
                return True
            else:
                logger.warning(f"Non-existent server link attempted to be removed by {admin_user}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing server link: {e}")
            return False
    
    async def get_server_status(self) -> dict:
        """
        Get status from manually configured server status file
        """
        try:
            import json
            import os
            
            status_file = os.path.join("config", "server_status.json")
            
            # Read from status file
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status = json.load(f)
            else:
                # Default status if file doesn't exist
                status = {
                    'online': True,
                    'player_count': 0,
                    'current_rp': "No active RP session",
                    'last_updated': "Not set",
                    'updated_by': "System"
                }
            
            # Add server name
            status['server_name'] = "Homeland RP | Private Server"
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting server status: {e}")
            return {
                'online': False,
                'player_count': 0,
                'current_rp': "Status unavailable",
                'last_updated': "Error",
                'updated_by': "System",
                'server_name': "Homeland RP | Private Server"
            }
    
    async def update_server_status(self, player_count: int, current_rp: str, updated_by: str) -> bool:
        """
        Update server status information (Owner/Admin only)
        """
        try:
            import json
            import os
            import datetime
            
            status_file = os.path.join("config", "server_status.json")
            
            new_status = {
                'online': True,
                'player_count': player_count,
                'current_rp': current_rp,
                'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'updated_by': updated_by
            }
            
            # Create config directory if it doesn't exist
            os.makedirs("config", exist_ok=True)
            
            # Write to status file
            with open(status_file, 'w') as f:
                json.dump(new_status, f, indent=2)
            
            logger.info(f"Server status updated by {updated_by}: {player_count} players, RP: {current_rp}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating server status: {e}")
            return False
    
    def validate_roblox_link(self, link: str) -> bool:
        """
        Validate if a link is a proper Roblox private server link
        """
        # Basic validation for Roblox private server URLs
        roblox_patterns = [
            'roblox.com/games/',
            'www.roblox.com/games/',
            'roblox.com/share?link='
        ]
        
        return any(pattern in link.lower() for pattern in roblox_patterns)
