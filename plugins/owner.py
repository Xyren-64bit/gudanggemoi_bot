# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import os
import subprocess
import sys
import asyncio
from dotenv import load_dotenv, set_key
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import Message
from bot import Bot
from database.sql import full_userbase 
from config import ADMINS, LOGGER

@Bot.on_message(filters.command("edit") & filters.user(ADMINS))
async def edit_variable(client: Bot, message: Message):
    """Edit variables in config.env."""

    cmd = message.text.split(" ", 2)
    if len(cmd) < 3:
        return await message.reply_text("Format salah! Gunakan: /edit VARIABEL nilai")

    var_name, new_value = cmd[1], cmd[2]

    # Check if the variable exists in config.env
    if var_name not in os.environ:
        return await message.reply_text(f"Variabel {var_name} tidak ditemukan dalam config.env")

    # Update the variable in config.env
    set_key("config.env", var_name, new_value)

    await message.reply_text(
        f"Berhasil mengubah nilai variabel {var_name} menjadi {new_value}.\n"
        "Gunakan perintah /restart untuk menerapkan perubahan."
    )


@Bot.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(client: Bot, message: Message):
    """Performs a hard restart of the bot."""

    restart_message = await message.reply_text("**Melakukan hard restart...**")

    load_dotenv("config.env", override=True) 
    
    del sys.modules["config"]

    async def restart_task():
        try:
            await asyncio.wait_for(client.stop(), timeout=10)
        except asyncio.TimeoutError:
            LOGGER(__name__).warning("Penghentian bot timeout. Memaksa keluar.")
        finally:
            LOGGER(__name__).info("Restarting bot...")
            subprocess.Popen([sys.executable, "main.py"])

    asyncio.create_task(restart_task())

    await asyncio.sleep(5)
    await restart_message.edit("✅ Proses restart selesai. Bot berhasil diaktifkan kembali.")


@Bot.on_message(filters.command("silent") & filters.user(ADMINS))
async def silent_all_media(client: Bot, message: Message):
    """
    This function deletes all media messages (except text and commands) from the first 1000 users in the database.
    """

    await message.reply_text("Memulai proses silent...")

    users = await full_userbase()
    deleted_count = 0
    user_count = 0

    for user in users:
        if user_count >= 1000: 
            break

        user_id = user.id
        user_count += 1

        try:
            async for user_message in client.get_chat_history(user_id):
                if (
                    user_message.media
                    and user_message.media in (enums.MessageMediaType.PHOTO, enums.MessageMediaType.VIDEO)
                    and user_message.caption
                    and not user_message.text.startswith("/")
                ):
                    await client.delete_messages(user_id, user_message.id)
                    deleted_count += 1
                    await asyncio.sleep(2) 
        except (FloodWait, UserIsBlocked, InputUserDeactivated):
            continue

        await asyncio.sleep(120)  

    await message.reply_text(f"Proses silent selesai!\n\nMedia berhasil dihapus dari {deleted_count} ID pengguna.")
