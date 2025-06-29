from keep_alive import keep_alive
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

        self.last_auto_response = {}

    async def setup_hook(self):
        logger.info("Setting up bot commands...")
        await setup_commands(self)
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

    async def on_ready(self):
        logger.info(f'{self.user} has logged in successfully!')
        logger.info(f'Bot is connected to {len(self.guilds)} guild(s)')
        activity = discord.Activity(type=discord.ActivityType.watching, name="Homeland RP Server")
        await self.change_presence(activity=activity)
        for guild in self.guilds:
            logger.info(f'Connected to guild: {guild.name} (ID: {guild.id})')

    async def on_message(self, message):
        if message.author.bot:
            return

        if "code" in message.content.lower():
            import time
            current_time = time.time()
            channel_id = message.channel.id

            if channel_id in self.last_auto_response:
                if current_time - self.last_auto_response[channel_id] < 30:
                    return

            try:
                from bot.server_manager import ServerManager
                server_manager = ServerManager()
                server_link = await server_manager.get_server_link()

                embed = discord.Embed(
                    title="🎮 Homeland RP Server",
                    description="Click the button below to join our private server!",
                    color=discord.Color.blue()
                )

                view = discord.ui.View(timeout=300)
                button = discord.ui.Button(
                    label="Join Server",
                    style=discord.ButtonStyle.link,
                    url=server_link,
                    emoji="🎮"
                )
                view.add_item(button)

                await message.channel.send(embed=embed, view=view)
                self.last_auto_response[channel_id] = current_time
                logger.info(f"Auto-sent server button to {message.author} in response to 'code'")

            except Exception as e:
                logger.error(f"Error auto-sending server link: {e}")
                await message.channel.send("Server not available right now.")

        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f"Command error in {ctx.command}: {error}")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to execute this command.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Member not found. Please check the username and try again.")
        else:
            await ctx.send("❌ An error occurred while processing your command.")

# ✅ SOLO UNA FUNCIÓN main CON EL keep_alive ADENTRO
async def main():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not found!")
        return

    keep_alive()  # ✅ Esto mantiene vivo el bot en Replit

    bot = HomelandBot()
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
    finally:
        await bot.close()

# Ejecutar el bot
if __name__ == "__main__":
    asyncio.run(main())
