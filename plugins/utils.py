# Credits: @mrismanaziz
# FROM File-Sharing-Man <https://github.com/mrismanaziz/File-Sharing-Man/>
# t.me/SharingUserbot & t.me/Lunatic0de

import os

from bot import Bot
from config import (
    ADMINS,
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    DB_URI,
    FORCE_MSG,
    FORCE_SUB_CHANNEL,
    FORCE_SUB_GROUP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGGER,
    OWNER,
    PROTECT_CONTENT,
    START_MSG,
    TG_BOT_TOKEN,
)
from pyrogram import filters
from pyrogram.types import Message


@Bot.on_message(filters.command("logs") & filters.user(ADMINS))
async def get_bot_logs(client: Bot, m: Message):
    bot_log_path = "logs.txt"
    if os.path.exists(bot_log_path):
        try:
            await m.reply_document(
                bot_log_path,
                quote=True,
                caption="<b>Ini Logs Bot ini</b>",
            )
        except Exception as e:
            os.remove(bot_log_path)
            LOGGER(__name__).warning(e)
    elif not os.path.exists(bot_log_path):
        await m.reply_text("❌ <b>Tidak ada log yang ditemukan!</b>")


@Bot.on_message(filters.command("vars") & filters.user(ADMINS))
async def varsFunc(client: Bot, message: Message):
    Man = await message.reply_text("Tunggu Sebentar...")
    text = f"""<u><b>CONFIG VARS</b></u> @{client.username}
APP_ID = <code>{APP_ID}</code>
API_HASH = <code>{API_HASH}</code>
TG_BOT_TOKEN = <code>{TG_BOT_TOKEN}</code>
DATABASE_URL = <code>{DB_URI}</code>
OWNER = <code>{OWNER}</code>
ADMINS = <code>{ADMINS}</code>
    
<u><b>CUSTOM VARS</b></u>
CHANNEL_ID = <code>{CHANNEL_ID}</code>
FORCE_SUB_CHANNEL = <code>{FORCE_SUB_CHANNEL}</code>
FORCE_SUB_GROUP = <code>{FORCE_SUB_GROUP}</code>
PROTECT_CONTENT = <code>{PROTECT_CONTENT}</code>
START_MSG = <code>{START_MSG}</code>
FORCE_MSG = <code>{FORCE_MSG}</code>

<u><b>HEROKU CONFIGVARS</b></u>
HEROKU_APP_NAME = <code>{HEROKU_APP_NAME}</code>
HEROKU_API_KEY = <code>{HEROKU_API_KEY}</code>
    """
    await Man.edit_text(text)


@Bot.on_message(filters.command("edit") & filters.user(ADMINS))
async def edit_multiple_vars(client: Bot, message: Message):
    """Mengedit satu atau beberapa variabel konfigurasi dalam file config.env dan selalu restart bot."""
    if len(message.command) < 3:
        await message.reply_text("**Penggunaan:**\n/edit [-b] nama_variabel1 nilai_baru1 [; nama_variabel2 nilai_baru2 ...]")
        return

    var_pairs = message.text.split(" ", 1)[1].strip().split(";")  

    for var_pair in var_pairs:
        try:
            var_name, new_value = var_pair.strip().split(" ")
            set_key("config.env", var_name, new_value)
            await message.edit_text(f"✅ Variabel **{var_name}** berhasil diubah menjadi **{new_value}**")
        except ValueError:
            await message.reply_text(f"❌ Format tidak valid untuk pasangan: {var_pair}")

    restart_message = await message.reply_text("🔄 Bot akan direstart...")     
    subprocess.Popen(["python3", "main.py"])
    await asyncio.sleep(10)
    await restart_message.edit_text(f"[🔥 BERHASIL DIAKTIFKAN! 🔥]\n\nBOT Dibuat oleh @{OWNER}")
    await client.stop()
