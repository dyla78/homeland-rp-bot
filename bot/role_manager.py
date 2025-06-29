import discord
import logging
from typing import Tuple, Dict, List
from config.settings import BOT_CONFIG

logger = logging.getLogger(__name__)

class RoleManager:
    def __init__(self):
        self.protected_roles = BOT_CONFIG['protected_roles']
        self.role_categories = BOT_CONFIG['role_categories']
    
    async def add_role(self, member: discord.Member, role: discord.Role, moderator: discord.Member) -> Tuple[bool, str]:
        """
        Add a role to a member
        Returns: (success: bool, message: str)
        """
        try:
            # Check if role is protected
            if role.name.lower() in [r.lower() for r in self.protected_roles]:
                return False, f"The role '{role.name}' is protected and cannot be assigned through the bot."
            
            # Check if member already has the role
            if role in member.roles:
                return False, f"{member.mention} already has the role '{role.name}'."
            
            # Check bot permissions
            if not member.guild.me.guild_permissions.manage_roles:
                return False, "I don't have permission to manage roles."
            
            # Check role hierarchy
            if role.position >= member.guild.me.top_role.position:
                return False, f"I cannot assign the role '{role.name}' as it's higher than my highest role."
            
            # Add the role
            await member.add_roles(role, reason=f"Role added by {moderator}")
            
            message = f"Successfully added the role '{role.name}' to {member.mention}."
            logger.info(f"Role {role.name} added to {member} by {moderator}")
            
            return True, message
            
        except discord.Forbidden:
            return False, "I don't have permission to manage this role."
        except discord.HTTPException as e:
            logger.error(f"HTTP error adding role: {e}")
            return False, "Failed to add role due to a Discord API error."
        except Exception as e:
            logger.error(f"Unexpected error adding role: {e}")
            return False, "An unexpected error occurred while adding the role."
    
    async def remove_role(self, member: discord.Member, role: discord.Role, moderator: discord.Member) -> Tuple[bool, str]:
        """
        Remove a role from a member
        Returns: (success: bool, message: str)
        """
        try:
            # Check if role is protected
            if role.name.lower() in [r.lower() for r in self.protected_roles]:
                return False, f"The role '{role.name}' is protected and cannot be removed through the bot."
            
            # Check if member has the role
            if role not in member.roles:
                return False, f"{member.mention} doesn't have the role '{role.name}'."
            
            # Check bot permissions
            if not member.guild.me.guild_permissions.manage_roles:
                return False, "I don't have permission to manage roles."
            
            # Check role hierarchy
            if role.position >= member.guild.me.top_role.position:
                return False, f"I cannot remove the role '{role.name}' as it's higher than my highest role."
            
            # Remove the role
            await member.remove_roles(role, reason=f"Role removed by {moderator}")
            
            message = f"Successfully removed the role '{role.name}' from {member.mention}."
            logger.info(f"Role {role.name} removed from {member} by {moderator}")
            
            return True, message
            
        except discord.Forbidden:
            return False, "I don't have permission to manage this role."
        except discord.HTTPException as e:
            logger.error(f"HTTP error removing role: {e}")
            return False, "Failed to remove role due to a Discord API error."
        except Exception as e:
            logger.error(f"Unexpected error removing role: {e}")
            return False, "An unexpected error occurred while removing the role."
    
    async def get_roles_info(self, guild: discord.Guild) -> Dict[str, List[Dict]]:
        """
        Get information about roles in the guild
        Returns: Dictionary with role categories and their roles
        """
        try:
            roles_info = {}
            
            # Get all roles excluding @everyone
            all_roles = [role for role in guild.roles if role.name != "@everyone"]
            
            # Categorize roles
            for category, role_names in self.role_categories.items():
                roles_info[category] = []
                
                for role in all_roles:
                    # Check if role matches any in the category (case insensitive)
                    if any(role_name.lower() in role.name.lower() for role_name in role_names):
                        roles_info[category].append({
                            'name': role.name,
                            'members': len(role.members),
                            'color': str(role.color),
                            'position': role.position
                        })
                
                # Sort by position (higher position = higher in hierarchy)
                roles_info[category].sort(key=lambda x: x['position'], reverse=True)
            
            # Add uncategorized roles
            categorized_roles = set()
            for category_roles in roles_info.values():
                categorized_roles.update(role['name'] for role in category_roles)
            
            uncategorized = []
            for role in all_roles:
                if role.name not in categorized_roles and not role.managed:
                    uncategorized.append({
                        'name': role.name,
                        'members': len(role.members),
                        'color': str(role.color),
                        'position': role.position
                    })
            
            if uncategorized:
                uncategorized.sort(key=lambda x: x['position'], reverse=True)
                roles_info['Other Roles'] = uncategorized
            
            return roles_info
            
        except Exception as e:
            logger.error(f"Error getting roles info: {e}")
            return {"Error": [{"name": "Unable to fetch role information", "members": 0}]}
    
    def is_role_manageable(self, role: discord.Role, bot_member: discord.Member) -> bool:
        """
        Check if a role can be managed by the bot
        """
        # Check if role is protected
        if role.name.lower() in [r.lower() for r in self.protected_roles]:
            return False
        
        # Check role hierarchy
        if role.position >= bot_member.top_role.position:
            return False
        
        # Check if role is managed by integration
        if role.managed:
            return False
        
        return True
