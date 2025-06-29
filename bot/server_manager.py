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
        Get status of all configured servers (placeholder for future implementation)
        """
        try:
            status = {
                'total_servers': len(self.server_links),
                'active_servers': len(self.server_links),  # Assume all active for now
                'last_updated': 'Not implemented'
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting server status: {e}")
            return {'error': 'Unable to retrieve server status'}
    
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
