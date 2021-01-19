from pyrogram import Client, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(group=-1)
async def CheckUserinChannel(c, m):
    # channel User checker
    if not await inChannel(c, m):
        try:
            await sendJoinmsg(m)
        except :
            pass
        finally:
            raise StopPropagation





async def inChannel(client,message):
        try: 
            await client.get_chat_member("aryan_bots", message.from_user.id)
            return True
        except Exception :
            return False




async def sendJoinmsg(message):
    joinButton=InlineKeyboardMarkup([

        [InlineKeyboardButton("Join Update Channel", url="https://t.me/aryan_bots")]  
    
    ])
    await message.reply_text("join channel To access Bot 🔐 " ,reply_markup = joinButton)