import os
import discord
from discord.ext import commands
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

bot = commands.Bot(command_prefix='!', intents=intents)

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