from pyrogram import Client, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(group=-1)
async def checkauthfunc(c, m):
    # channel User checker
    if not await inChannel(c, m):
        await sendJoinmsg(m)
        raise StopPropagation





async def inChannel(client,message):
        try: 
            await client.get_chat_member("aryan_bots", message.from_user.id)
            return True
        except Exception :
            return False




async def sendJoinmsg(message):
    joinButton=InlineKeyboardMarkup([

        [InlineKeyboardButton("Join", url="https://t.me/aryan_bots")]  
    
    ])
    await message.reply_text("join channel To access Bot 🔐 " ,reply_markup = joinButton)