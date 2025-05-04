# Discord English-Only Chat Filter Bot

A Discord bot that automatically moderates specific text channels by ensuring all messages are in English. Perfect for study groups and focus rooms where maintaining a common language is important.

## Features

- Monitors specified text channels for non-English messages
- Automatically deletes messages containing Arabic characters
- Sends temporary warnings to users who post non-English messages
- Ignores messages from other bots
- Lightweight and efficient character detection

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd discord-english-only-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   - Create a new file named `.env` in the project root
   - Add your bot token and channel IDs:
     ```
     BOT_TOKEN=your_bot_token_here
     ENGLISH_ONLY_CHANNEL_IDS=channel_id1,channel_id2,channel_id3
     ```

4. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a bot
   - Copy the bot token and add it to your `.env` file
   - Enable the following intents:
     - Message Content Intent
     - Server Members Intent

5. **Invite the bot to your server**
   - Use this URL (replace YOUR_CLIENT_ID with your bot's client ID):
     ```
     https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=3072&scope=bot
     ```

## Running the Bot

### Quick Start
```bash
python bot.py
```

### Running Continuously (Recommended)
To keep the bot running 24/7, even after closing the terminal:

1. **Install screen** (if not already installed)
   ```bash
   # On macOS
   brew install screen
   
   # On Ubuntu/Debian
   sudo apt-get install screen
   ```

2. **Create a new screen session**
   ```bash
   screen -S discordbot
   ```

3. **Start the bot in the screen session**
   ```bash
   cd /path/to/bot/directory
   source venv/bin/activate
   python bot.py
   ```

4. **Detach from screen session**
   - Press `Ctrl + A` followed by `D`

### Managing the Bot

- **Check if bot is running**
  ```bash
  screen -ls
  ```

- **View bot output**
  ```bash
  screen -r discordbot
  ```

- **Stop the bot**
  1. Reattach to screen: `screen -r discordbot`
  2. Press `Ctrl + C` to stop the bot
  3. Type `exit` to close the screen session

- **Restart the bot**
  1. Reattach to screen: `screen -r discordbot`
  2. Stop the bot with `Ctrl + C`
  3. Start it again: `python bot.py`
  4. Detach with `Ctrl + A` then `D`

## Permissions Required

The bot needs the following permissions:
- Read Messages
- Send Messages
- Manage Messages

## Testing

The bot will:
- ✅ Allow English messages
- ❌ Delete messages containing Arabic characters
- ✅ Ignore bot messages
- ✅ Send temporary warnings for violations

## Contributing

Feel free to submit issues and enhancement requests! 