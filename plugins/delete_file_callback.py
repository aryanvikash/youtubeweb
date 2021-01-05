import asyncio
import os
from pyrogram import (Client,ContinuePropagation,StopPropagation,filters)
from bot import usersLinks


@Client.on_callback_query(filters.regex(r"^del\|\|"))
async def catch_youtube_dldata(c, q):
    userid = q.message.chat.id
    cb_data = q.data.strip()
    uuidd = cb_data.split("||")[-1]
    
    print(cb_data)
    try:
        filename = usersLinks[uuidd]
    except :
        await q.edit_message_text(f"`{filename}` \n\n#File_not_Avalible")
        return    
    try:
        os.remove(os.path.join("downloads",str(userid),filename))
        await q.edit_message_text(f"`{filename}` \n#File_Deleted")
    except FileNotFoundError:
        await q.edit_message_text(f"`{filename}` \n\n#File_not_Avalible_or_Already_Deleted")

    