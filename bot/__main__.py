from pyrogram import Client ,idle
import config
import asyncio
# import threading
# from web import app

BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH


plugins = dict(
    root="plugins",
)


pyro =  Client(
    "YouTubeDlBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    workers=50
)

# threading.Thread(target=app.run, daemon=True).start()

pyro.run()

