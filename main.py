import discord
from discord.ext import commands
import asyncio
import logging
import os
from config.settings import BOT_CONFIG
from utils.logger import setup_logger
from bot.commands import setup_commands

# Setup logging
logger = setup_logger()

class HomelandBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        
        # Cooldown tracking for auto-responses
        self.last_auto_response = {}
        
    async def setup_hook(self):
        """Called when the bot is starting up"""
        logger.info("Setting up bot commands...")
        await setup_commands(self)
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'{self.user} has logged in successfully!')
        logger.info(f'Bot is connected to {len(self.guilds)} guild(s)')
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="Homeland RP Server"
        )
        await self.change_presence(activity=activity)
        
        # Log guild information
        for guild in self.guilds:
            logger.info(f'Connected to guild: {guild.name} (ID: {guild.id})')
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Don't respond to bot messages
        if message.author.bot:
            return
        
        # Check if message contains "code" (case insensitive)
        if "code" in message.content.lower():
            # Check cooldown (30 seconds per channel)
            import time
            current_time = time.time()
            channel_id = message.channel.id
            
            if channel_id in self.last_auto_response:
                if current_time - self.last_auto_response[channel_id] < 30:
                    return  # Skip if within cooldown
            
            try:
                from bot.server_manager import ServerManager
                server_manager = ServerManager()
                server_link = await server_manager.get_server_link()
                
                # Create button view
                view = discord.ui.View(timeout=300)  # 5 minute timeout
                button = discord.ui.Button(
                    label="Join Server",
                    style=discord.ButtonStyle.primary,
                    url=server_link,
                    emoji="🎮"
                )
                view.add_item(button)
                
                # Send message with button
                await message.channel.send("🎮 **Homeland RP Server**", view=view)
                
                # Update cooldown
                self.last_auto_response[channel_id] = current_time
                logger.info(f"Auto-sent server button to {message.author} in response to 'code' keyword")
                
            except Exception as e:
                logger.error(f"Error auto-sending server link: {e}")
                await message.channel.send("Server not available right now.")
        
        # Process commands normally
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands
        
        logger.error(f"Command error in {ctx.command}: {error}")
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to execute this command.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Member not found. Please check the username and try again.")
        else:
            await ctx.send("❌ An error occurred while processing your command.")

async def main():
    """Main function to run the bot"""
    # Get bot token from environment variables
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not found!")
        return
    
    # Create and run bot
    bot = HomelandBot()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
