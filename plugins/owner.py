# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import os
import sys
from dotenv import set_key
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS, LOGGER

@Bot.on_message(filters.command("edit") & filters.user(ADMINS))
async def edit_variable(client: Bot, message: Message):
    """Edit variables in config.env and trigger a soft restart."""

    cmd = message.text.split(" ", 2)
    if len(cmd) < 3:
        return await message.reply_text("**Format salah!** Gunakan: `/edit VARIABEL nilai`")

    var_name = cmd[1]
    new_value = cmd[2]

    # Update the variable in config.env
    set_key("config.env", var_name, new_value)

    # Reload config module
    from importlib import reload
    import config
    reload(config)

    # Soft restart the bot
    await message.reply_text("**Variabel berhasil diubah! Melakukan soft restart...**")
    args = [sys.executable, "-m", "bot"]
    os.execv(sys.executable, args)
