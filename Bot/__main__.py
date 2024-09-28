import os
import logging
from . import client
from aiohttp import ClientSession
from pyrogram import idle
from flask import Flask
import threading

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Flask setup for port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Default port is 8080
    app.run(host='0.0.0.0', port=port)

# Main bot function
async def main():
    await client.startup()
    await client.bot.set_bot_commands(client.config.BOT_COMMANDS)
    session = ClientSession()
    client.session = session
    if client.config.AUTH_USERS:
        client.config.AUTH_USERS.append(client.config.OWNER_ID)
    client.logger.info(f'{client.bot.me.first_name} Started!')
    await idle()

if __name__ == '__main__':
    # Ensure download directory exists
    if not os.path.isdir(client.config.DOWNLOAD_LOCATION):
        os.makedirs(client.config.DOWNLOAD_LOCATION)

    # Start Flask server in a new thread
    threading.Thread(target=run_flask).start()

    # Run the bot
    client.run(main())
