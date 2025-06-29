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
    
    @bot.tree.command(name="addrole", description="Add a role to a user (Admin/Moderator only)")
    @app_commands.describe(
        member="The member to add the role to",
        role="The role to add"
    )
    async def add_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Add a role to a member"""
        if not has_permission(interaction.user, PermissionLevel.MODERATOR):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return
        
        try:
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
            await interaction.response.send_message(
                "❌ An error occurred while adding the role.",
                ephemeral=True
            )
    
    @bot.tree.command(name="removerole", description="Remove a role from a user (Admin/Moderator only)")
    @app_commands.describe(
        member="The member to remove the role from",
        role="The role to remove"
    )
    async def remove_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        if not has_permission(interaction.user, PermissionLevel.MODERATOR):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return
        
        try:
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
            await interaction.response.send_message(
                "❌ An error occurred while removing the role.",
                ephemeral=True
            )
    
    @bot.tree.command(name="roleinfo", description="Get information about server roles")
    async def role_info(interaction: discord.Interaction):
        """Display information about available roles"""
        try:
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
            value="• `/server` - Get private server link\n• `/addrole` - Add role to user\n• `/removerole` - Remove role from user\n• `/roleinfo` - View role information",
            inline=False
        )
        
        embed.add_field(
            name="👥 Guild Info",
            value=f"Serving {len(bot.guilds)} server(s)",
            inline=True
        )
        
        embed.set_footer(text="Homeland RP | Official Bot • Made for the community")
        await interaction.response.send_message(embed=embed)
    
    logger.info("All commands have been set up successfully")
