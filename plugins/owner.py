import os
import subprocess
from dotenv import set_key
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS, LOGGER

@Bot.on_message(filters.command("edit") & filters.user(ADMINS))
async def edit_variable(client: Bot, message: Message):
    """Edit variables in config.env and trigger a restart using 'bash start'."""

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
    restart_message = await message.reply_text(
        f"<b>Berhasil mengubah nilai variabel {var_name} menjadi {new_value}.<\b>\n"
        "Melakukan restart bot untuk menerapkan perubahan..."
    )

    # Trigger a restart using 'bash start'
    try:
        subprocess.Popen(["bash", "start"])
    except FileNotFoundError:
        await restart_message.edit("❌ Tidak dapat menemukan file 'start'. Pastikan file tersebut ada dan memiliki izin eksekusi.")
    except Exception as e:
        await restart_message.edit(f"❌ Terjadi kesalahan saat me-restart: {e}")
    else:
        # Edit the message after successful restart
        await restart_message.edit(
            f"✅ Bot berhasil diaktifkan kembali dengan nilai baru untuk `{var_name}`: `{new_value}`"
        )
