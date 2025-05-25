import os
from telethon import TelegramClient, events

bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

environment = os.getenv('ENV', default='dev')

assert bot_token is not None, 'BOT_TOKEN was not set, bot cannot initilise'
assert api_id is not None, 'API_ID was not set, bot cannot initilise'
assert api_hash is not None, 'API_HASH was not set, bot cannot initilise'

bot_client = TelegramClient('mu2_session', api_id, api_hash).start(bot_token=bot_token)


@bot_client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Started')
    raise events.StopPropagation

@bot_client.on(events.NewMessage)
async def echo(event):
    await event.respond(event.text)

def main():
    # Start the bot
    bot_client.run_until_disconnected()

main()