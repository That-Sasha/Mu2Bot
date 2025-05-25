import logging
import os
from telethon import TelegramClient, events
from command_handler import file_senders
from e621_wrapper import E621

# Setup logging
logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger()

# Get env vars
bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
env = os.getenv('ENV', default='dev')

# Validate mandatory env vars
assert bot_token is not None, 'BOT_TOKEN was not set, bot cannot initilise'
assert api_id is not None, 'API_ID was not set, bot cannot initilise'
assert api_hash is not None, 'API_HASH was not set, bot cannot initilise'

# Setup e621 client
e6_client = E621() # need to add blacklist

# Create client for the bot
bot_client = TelegramClient(f'/data/mu2-{env}_session', api_id, api_hash).start(bot_token=bot_token)

def init(client):
    bot_client = client

@bot_client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Started')
    raise events.StopPropagation

@bot_client.on(events.NewMessage(pattern='^/(e6|8ball|bomb)\s*(.*)'))
async def e6(event):

    command = event.pattern_match.group(1)
    arguments = event.pattern_match.group(2)

    images = file_senders(e6_client, command, arguments)

    if images:
        await bot_client.send_file(event.sender_id, images, caption='Here ya go!')
    else:
        await event.respond('Sorry! I couldn\'t find an image. Check your tags or try later')

    raise events.StopPropagation

@bot_client.on(events.NewMessage)
async def echo(event):
    await event.respond('Unhandled event! uh oh')

def main():
    # Start the bot
    bot_client.run_until_disconnected()

main()