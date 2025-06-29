import discord
from discord.ext import commands
from discord import app_commands
import logging
from bot.role_manager import RoleManager
from bot.server_manager import ServerManager
from bot.permissions import has_permission, PermissionLevel
from config.settings import BOT_CONFIG

logger = logging.getLogger(__name__)

async def setup_commands(bot):
    """Setup all bot commands"""
    role_manager = RoleManager()
    server_manager = ServerManager()
    
    @bot.tree.command(name="server", description="Get a Roblox private server link for Homeland RP")
    async def get_server(interaction: discord.Interaction):
        """Provide a Roblox private server link"""
        try:
            server_link = await server_manager.get_server_link()
            
            embed = discord.Embed(
                title="🎮 Homeland RP Private Server",
                description=f"Join our private server using the link below:",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Server Link",
                value=f"[Click here to join!]({server_link})",
                inline=False
            )
            embed.add_field(
                name="📋 Instructions",
                value="1. Click the link above\n2. Wait for Roblox to load\n3. Have fun roleplaying!",
                inline=False
            )
            embed.set_footer(text="Homeland RP | Official Bot")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Server link provided to {interaction.user} in {interaction.guild}")
            
        except Exception as e:
            logger.error(f"Error providing server link: {e}")
            await interaction.response.send_message(
                "❌ Unable to retrieve server link at this time. Please try again later.",
                ephemeral=True
            )
    
    @bot.tree.command(name="addrole", description="Add a role to a user (Owner only)")
    @app_commands.describe(
        member="The member to add the role to",
        role="The role to add"
    )
    async def add_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Add a role to a member"""
        if not has_permission(interaction.user, PermissionLevel.OWNER):
            await interaction.response.send_message(
                "❌ Only the bot owner can use this command.",
                ephemeral=True
            )
            return
        
        try:
            # Ensure we have a guild member context
            if not isinstance(interaction.user, discord.Member):
                await interaction.response.send_message(
                    "❌ This command can only be used in a server.",
                    ephemeral=True
                )
                return
            
            success, message = await role_manager.add_role(member, role, interaction.user)
            
            if success:
                embed = discord.Embed(
                    title="✅ Role Added Successfully",
                    description=message,
                    color=discord.Color.green()
                )
                embed.set_footer(text="Homeland RP | Official Bot")
                await interaction.response.send_message(embed=embed)
                logger.info(f"Role {role.name} added to {member} by {interaction.user}")
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
                
        except Exception as e:
            logger.error(f"Error adding role: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ An error occurred while adding the role.",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        "❌ An error occurred while adding the role.",
                        ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}")
    
    @bot.tree.command(name="removerole", description="Remove a role from a user (Owner only)")
    @app_commands.describe(
        member="The member to remove the role from",
        role="The role to remove"
    )
    async def remove_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        if not has_permission(interaction.user, PermissionLevel.OWNER):
            await interaction.response.send_message(
                "❌ Only the bot owner can use this command.",
                ephemeral=True
            )
            return
        
        try:
            # Ensure we have a guild member context
            if not isinstance(interaction.user, discord.Member):
                await interaction.response.send_message(
                    "❌ This command can only be used in a server.",
                    ephemeral=True
                )
                return
            
            success, message = await role_manager.remove_role(member, role, interaction.user)
            
            if success:
                embed = discord.Embed(
                    title="✅ Role Removed Successfully",
                    description=message,
                    color=discord.Color.orange()
                )
                embed.set_footer(text="Homeland RP | Official Bot")
                await interaction.response.send_message(embed=embed)
                logger.info(f"Role {role.name} removed from {member} by {interaction.user}")
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
                
        except Exception as e:
            logger.error(f"Error removing role: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ An error occurred while removing the role.",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        "❌ An error occurred while removing the role.",
                        ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}")
    
    @bot.tree.command(name="roleinfo", description="Get information about server roles")
    async def role_info(interaction: discord.Interaction):
        """Display information about available roles"""
        try:
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server.",
                    ephemeral=True
                )
                return
            
            roles_info = await role_manager.get_roles_info(interaction.guild)
            
            embed = discord.Embed(
                title="📋 Server Roles Information",
                description="Here are the available roles in this server:",
                color=discord.Color.blue()
            )
            
            for category, roles in roles_info.items():
                if roles:
                    role_list = "\n".join([f"• {role['name']} - {role['members']} members" for role in roles])
                    embed.add_field(
                        name=f"{category}",
                        value=role_list,
                        inline=False
                    )
            
            embed.set_footer(text="Homeland RP | Official Bot")
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error getting role info: {e}")
            await interaction.response.send_message(
                "❌ Unable to retrieve role information.",
                ephemeral=True
            )
    
    @bot.tree.command(name="botinfo", description="Get information about the bot")
    async def bot_info(interaction: discord.Interaction):
        """Display bot information"""
        embed = discord.Embed(
            title="🤖 Homeland RP | Official Bot",
            description="Your official bot for Homeland RP server management!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📋 Features",
            value="• Private server link distribution\n• Role management system\n• Permission-based commands\n• Activity logging",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Commands",
            value="• `/server` - Get private server link\n• `/serverstatus` - Check server status\n• `/updatestatus` - Update server info (Owner/Admin only)\n• `/addrole` - Add role to user (Owner only)\n• `/removerole` - Remove role from user (Owner only)\n• `/roleinfo` - View role information",
            inline=False
        )
        
        embed.add_field(
            name="👥 Guild Info",
            value=f"Serving {len(bot.guilds)} server(s)",
            inline=True
        )
        
        embed.set_footer(text="Homeland RP | Official Bot • Made for the community")
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name="serverstatus", description="Check Roblox server status and player count")
    async def server_status(interaction: discord.Interaction):
        """Display server status information"""
        try:
            # Get server status from server manager
            status_info = await server_manager.get_server_status()
            
            embed = discord.Embed(
                title="🎮 Homeland RP Server Status",
                color=discord.Color.green() if status_info.get('online', False) else discord.Color.red()
            )
            
            # Server status
            status_emoji = "🟢" if status_info.get('online', False) else "🔴"
            embed.add_field(
                name=f"{status_emoji} Server Status",
                value="Online" if status_info.get('online', False) else "Offline",
                inline=True
            )
            
            # Player count
            player_count = status_info.get('player_count', 'Unknown')
            embed.add_field(
                name="👥 Players Count",
                value=f"{player_count}/50" if isinstance(player_count, int) else str(player_count),
                inline=True
            )
            
            # Current RP scenario
            current_rp = status_info.get('current_rp', 'No active RP session')
            embed.add_field(
                name="🎭 Current RP",
                value=current_rp,
                inline=False
            )
            
            # Last updated and updated by
            last_updated = status_info.get('last_updated', 'Not set')
            updated_by = status_info.get('updated_by', 'System')
            embed.set_footer(text=f"Last updated: {last_updated} by {updated_by} • Homeland RP | Official Bot")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Server status requested by {interaction.user}")
            
        except Exception as e:
            logger.error(f"Error getting server status: {e}")
            try:
                if not interaction.response.is_done():
                    embed = discord.Embed(
                        title="❌ Server Status Error",
                        description="Unable to retrieve server status at this time. Please try again later.",
                        color=discord.Color.red()
                    )
                    embed.set_footer(text="Homeland RP | Official Bot")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as followup_error:
                logger.error(f"Error sending server status error message: {followup_error}")
    
    @bot.tree.command(name="updatestatus", description="Update server player count and current RP (Owner/Admin only)")
    @app_commands.describe(
        player_count="Number of players currently online (0-50)",
        current_rp="Current roleplay scenario happening on the server"
    )
    async def update_status(interaction: discord.Interaction, player_count: int, current_rp: str):
        """Update server status information"""
        try:
            # Check permissions - Owner or Admin only
            if not has_permission(interaction.user, PermissionLevel.ADMIN):
                await interaction.response.send_message(
                    "❌ Only the owner or administrators can update server status.",
                    ephemeral=True
                )
                return
            
            # Validate player count
            if player_count < 0 or player_count > 50:
                await interaction.response.send_message(
                    "❌ Player count must be between 0 and 50.",
                    ephemeral=True
                )
                return
            
            # Validate RP description length
            if len(current_rp) > 200:
                await interaction.response.send_message(
                    "❌ Current RP description must be 200 characters or less.",
                    ephemeral=True
                )
                return
            
            # Update server status
            success = await server_manager.update_server_status(
                player_count, 
                current_rp, 
                str(interaction.user)
            )
            
            if success:
                embed = discord.Embed(
                    title="✅ Server Status Updated",
                    description="Server information has been updated successfully!",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="👥 Player Count",
                    value=f"{player_count}/50",
                    inline=True
                )
                embed.add_field(
                    name="🎭 Current RP",
                    value=current_rp,
                    inline=False
                )
                embed.set_footer(text=f"Updated by {interaction.user} • Homeland RP | Official Bot")
                await interaction.response.send_message(embed=embed)
                logger.info(f"Server status updated by {interaction.user}: {player_count} players, RP: {current_rp}")
            else:
                await interaction.response.send_message(
                    "❌ Failed to update server status. Please try again later.",
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error updating server status: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ An error occurred while updating server status.",
                        ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending update status error message: {followup_error}")
    
    logger.info("All commands have been set up successfully")
