import asyncio
import os
from urllib.parse import quote_plus
from pyrogram import (Client,ContinuePropagation,StopPropagation)
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli

from config import HostName


@Client.on_callback_query()
async def catch_youtube_dldata(c, q):
    userid = q.message.chat.id
    cb_data = q.data.strip()
    print(cb_data)
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

    if media_type.lower() == "audio":
        filename = await downloadaudiocli(audio_command)
        await q.edit_message_text(f"{HostName}/downloads/{userid}/{quote_plus(filename.split('/')[-1])}")

    if  media_type.lower() =="video":
        filename = await downloadvideocli(video_command)
        await q.edit_message_text(f"{HostName}/downloads/{userid}/{quote_plus(filename.split('/')[-1])}")


