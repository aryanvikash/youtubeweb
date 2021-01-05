import asyncio
import os
from urllib.parse import quote_plus
from pyrogram import (Client,ContinuePropagation,StopPropagation)
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli

from config import HostName
from bot import usersLinks
import uuid

@Client.on_callback_query()
async def catch_youtube_dldata(c, q):
    userid = q.message.chat.id
    cb_data = q.data.strip()
    if not cb_data.startswith("ytdata||"):
        raise StopPropagation

    yturl = cb_data.split("||")[-1]
    format_id = cb_data.split("||")[-2]
    media_type = cb_data.split("||")[-3].strip()
            
    

    filext = "%(title)s.%(ext)s"
    userdir = os.path.join(os.getcwd(), "downloads", str(q.message.chat.id))

    if not os.path.isdir(userdir):
        os.makedirs(userdir)
    await q.edit_message_reply_markup(
        InlineKeyboardMarkup([[InlineKeyboardButton("Downloading...", callback_data="down")]]))
    filepath = os.path.join(userdir, filext)
    # await q.edit_message_reply_markup([[InlineKeyboardButton("Processing..")]])

    audio_command = [
        "youtube-dl",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", format_id,
        "-o", filepath,
        yturl,

    ]

    video_command = [
        "youtube-dl",
        "-c",
        "--embed-subs",
        "-f", f"{format_id}+bestaudio",
        "-o", filepath,
        "--hls-prefer-ffmpeg", yturl]

    filepath = None
    Downloaderror = None

    if media_type.lower() == "audio":
        Downloaderror, filepath = await downloadaudiocli(audio_command)

    if  media_type.lower() == "video":
        Downloaderror, filepath = await downloadvideocli(video_command)

        
    if filepath:
        filenamePath = filepath.replace(" ","_")
        os.rename(filepath,filenamePath)
        downloadLink = f"{HostName}/downloads/{userid}/{quote_plus(os.path.basename(filenamePath))}"
        print(downloadLink)
        RandomId = uuid.uuid4().hex

        usersLinks[RandomId] = os.path.basename(filenamePath)
        downloadButton = InlineKeyboardMarkup([
            [InlineKeyboardButton("Download 🔗", url=downloadLink.strip(" "))],
            [InlineKeyboardButton("Delete 🚮",callback_data=f"del||{RandomId}")]
            ])
        downloadLink = f"{HostName}/downloads/{userid}/{quote_plus(os.path.basename(filenamePath))}"
        # await q.edit_message_text(downloadLink)
        await q.edit_message_reply_markup(downloadButton)
    else:
        await q.edit_message_text(f"{Downloaderror} \n#Download Error")


