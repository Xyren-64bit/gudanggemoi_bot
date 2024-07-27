# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import os
import subprocess
import sys
from dotenv import load_dotenv, set_key
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
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

    restart_message = await message.reply_text("Melakukan hard restart...")

    # Muat ulang variabel lingkungan sebelum restart
    load_dotenv("config.env", override=True)  # Muat ulang dengan menimpa nilai lama

    # Hard restart dengan menghentikan bot dan menjalankan ulang skrip
    await client.stop()
    subprocess.Popen([sys.executable, "main.py"])

    # Edit pesan setelah restart selesai
    await asyncio.sleep(5)  # Tunggu beberapa detik agar bot selesai restart
    await restart_message.edit("✅ Proses restart selesai. Bot berhasil diaktifkan kembali.")

    sys.exit(0)
