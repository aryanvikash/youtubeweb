from __future__ import unicode_literals
import youtube_dl
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.util import humanbytes
import asyncio


def buttonmap(item):
    quality = str(item['format'])
    if "tiny" in quality:
        return [InlineKeyboardButton(f"Audio 🎵 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]
    else:
        return [InlineKeyboardButton(f"{quality} 📹 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}")]

# Return a array of Buttons
def create_buttons(quailitylist):
    return map(buttonmap, quailitylist)


# extract Youtube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        qualityList = []
        r = ydl.extract_info(yturl, download=False)
        for format in r['formats']:
            # Filter dash video(without audio)
            if not "dash" in str(format['format']).lower():
                
                _format = str(format['format']).split("(")[-1].strip(")")
                qualityList.append(
                {"format": _format, "filesize": format['filesize'], "format_id": format['format_id'],
                 "yturl": yturl})

        return r['title'], r['thumbnail'], qualityList


#  Need to work on progress

# def downloadyt(url, fmid, custom_progress):
#     ydl_opts = {
#         'format': f"{fmid}+bestaudio",
#         "outtmpl": "test+.%(ext)s",
#         'noplaylist': True,
#         'progress_hooks': [custom_progress],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])


# https://github.com/SpEcHiDe/AnyDLBot

async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    filename = t_response.split("Merging formats into")[-1].split('"')[1]
    return e_response, filename


async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)

    return e_response ,t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()
