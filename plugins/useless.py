from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from database.database import *

# Combine ADMINS from config and admin_collection
combined_admins = set(ADMINS) | set(admins_collection)  # Using set to avoid duplicates


@Bot.on_message(filters.command('stats') & filters.user(combined_admins))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


@Bot.on_message(filters.private)
async def useless(_, message: Message):
    user_id = message.from_user.id

    # Check if the user is in the combined admin list
    if user_id in combined_admins:
        return  # Do not send USER_REPLY_TEXT to admins

    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
