import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_bot')

# Load environment variables
load_dotenv()

# Bot configuration
ENGLISH_ONLY_CHANNEL_IDS = [int(id.strip()) for id in os.getenv('ENGLISH_ONLY_CHANNEL_IDS', '').split(',') if id.strip()]
ARABIC_CHAT_CHANNEL_ID = 1081691213612199987
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class EnglishOnlyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        
    async def setup_hook(self):
        # Sync commands when bot starts
        await self.tree.sync()
        logger.info("Slash commands synced!")

bot = EnglishOnlyBot()

def contains_arabic(text):
    """Check if text contains Arabic characters."""
    arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ')
    has_arabic = any(char in arabic_chars for char in text)
    logger.info(f"Checking text for Arabic: '{text}' - Contains Arabic: {has_arabic}")
    return has_arabic

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Monitoring channels: {ENGLISH_ONLY_CHANNEL_IDS}')
    logger.info(f'Arabic chat channel: {ARABIC_CHAT_CHANNEL_ID}')

# Add a slash command
@bot.tree.command(name="english-only", description="Get information about English-only channels")
async def english_only(interaction: discord.Interaction):
    """Slash command to get information about English-only channels"""
    channels_info = "\n".join([f"<#{channel_id}>" for channel_id in ENGLISH_ONLY_CHANNEL_IDS])
    arabic_channel = f"<#{ARABIC_CHAT_CHANNEL_ID}>"
    
    embed = discord.Embed(
        title="English-Only Channels Information",
        description="Here are the channels where English is enforced:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="English-Only Channels",
        value=channels_info or "No channels configured",
        inline=False
    )
    embed.add_field(
        name="Arabic Chat Channel",
        value=arabic_channel,
        inline=False
    )
    embed.set_footer(text="Use /english-only to see this information again")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Only process messages in the specified channels
    if message.channel.id in ENGLISH_ONLY_CHANNEL_IDS:
        logger.info(f"Processing message in channel {message.channel.id}: {message.content}")
        try:
            # Skip empty messages
            if not message.content.strip():
                return

            # Check if message contains Arabic
            if contains_arabic(message.content):
                logger.info(f"Deleting message with Arabic: {message.content}")
                await message.delete()
                warning = await message.channel.send(
                    f"{message.author.mention}, English only in this channel please. "
                    f"For Arabic, please use <#{ARABIC_CHAT_CHANNEL_ID}>"
                )
                await warning.delete(delay=10)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    # Process commands
    await bot.process_commands(message)

# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'Error in {event}:', args[0])

# Run the bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        logger.error("No bot token found. Please set BOT_TOKEN in .env file")
        raise ValueError("No bot token found. Please set BOT_TOKEN in .env file")
    if not ENGLISH_ONLY_CHANNEL_IDS:
        logger.error("No channel IDs found. Please set ENGLISH_ONLY_CHANNEL_IDS in .env file")
        raise ValueError("No channel IDs found. Please set ENGLISH_ONLY_CHANNEL_IDS in .env file")
    
    logger.info("Starting bot...")
    bot.run(BOT_TOKEN) 