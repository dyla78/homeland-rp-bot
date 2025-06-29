import discord
import logging
from enum import Enum
from typing import List, Union
from config.settings import BOT_CONFIG

logger = logging.getLogger(__name__)

class PermissionLevel(Enum):
    """Permission levels for bot commands"""
    USER = 1
    MODERATOR = 2
    ADMIN = 3
    OWNER = 4

class PermissionManager:
    def __init__(self):
        self.admin_roles = BOT_CONFIG['admin_roles']
        self.moderator_roles = BOT_CONFIG['moderator_roles']
        self.owner_ids = BOT_CONFIG['owner_ids']
    
    def get_user_permission_level(self, user: Union[discord.Member, discord.User]) -> PermissionLevel:
        """
        Get the permission level of a user
        """
        try:
            # Check if user is bot owner
            if user.id in self.owner_ids:
                return PermissionLevel.OWNER
            
            # If user is not a member (DM context), return USER level
            if not isinstance(user, discord.Member):
                return PermissionLevel.USER
            
            # Check for admin permissions
            if user.guild_permissions.administrator:
                return PermissionLevel.ADMIN
            
            # Check admin roles
            user_roles = [role.name.lower() for role in user.roles]
            if any(admin_role.lower() in user_roles for admin_role in self.admin_roles):
                return PermissionLevel.ADMIN
            
            # Check moderator permissions
            if user.guild_permissions.manage_messages or user.guild_permissions.manage_roles:
                return PermissionLevel.MODERATOR
            
            # Check moderator roles
            if any(mod_role.lower() in user_roles for mod_role in self.moderator_roles):
                return PermissionLevel.MODERATOR
            
            return PermissionLevel.USER
            
        except Exception as e:
            logger.error(f"Error getting user permission level: {e}")
            return PermissionLevel.USER
    
    def has_permission(self, user: Union[discord.Member, discord.User], required_level: PermissionLevel) -> bool:
        """
        Check if user has the required permission level
        """
        try:
            user_level = self.get_user_permission_level(user)
            return user_level.value >= required_level.value
        except Exception as e:
            logger.error(f"Error checking permissions: {e}")
            return False
    
    def can_manage_user(self, moderator: discord.Member, target: discord.Member) -> bool:
        """
        Check if moderator can manage the target user
        """
        try:
            # Owner can manage anyone
            if moderator.id in self.owner_ids:
                return True
            
            # Can't manage users with higher or equal roles
            if target.top_role >= moderator.top_role:
                return False
            
            # Can't manage other moderators/admins unless you're admin+
            target_level = self.get_user_permission_level(target)
            moderator_level = self.get_user_permission_level(moderator)
            
            if target_level.value >= PermissionLevel.MODERATOR.value:
                return moderator_level.value > target_level.value
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking user management permissions: {e}")
            return False

# Create global permission manager instance
permission_manager = PermissionManager()

def has_permission(user: Union[discord.Member, discord.User], required_level: PermissionLevel) -> bool:
    """
    Global function to check permissions
    """
    return permission_manager.has_permission(user, required_level)

def get_permission_level(user: Union[discord.Member, discord.User]) -> PermissionLevel:
    """
    Global function to get user permission level
    """
    return permission_manager.get_user_permission_level(user)

def can_manage_user(moderator: discord.Member, target: discord.Member) -> bool:
    """
    Global function to check if moderator can manage target user
    """
    return permission_manager.can_manage_user(moderator, target)

def require_permission(level: PermissionLevel):
    """
    Decorator to require specific permission level for commands
    """
    def decorator(func):
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            if not has_permission(interaction.user, level):
                await interaction.response.send_message(
                    "❌ You don't have permission to use this command.",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator
