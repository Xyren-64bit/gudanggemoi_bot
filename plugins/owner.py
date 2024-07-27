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

    var_name, new_value = cmd[1], cmd[2]

    # Update the variable in config.env
    set_key("config.env", var_name, new_value)

    # Reload config module
    try:
        from importlib import reload
        import config
        reload(config)
    except ImportError:
        LOGGER(__name__).error("Gagal me-reload modul config.")
        return

    # Inform the admin about the successful change and restart
    await message.reply_text(
        f"Berhasil mengubah nilai variabel {var_name} menjadi {new_value}.\n"
        "Melakukan restart bot untuk menerapkan perubahan..."
    )

    # Soft restart the bot
    args = [sys.executable, "main.py"]
    os.execv(sys.executable, args)
