from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from database.database import admins_collection  # Ensure this is the correct import

# Fetch admin IDs from the database
db_admins = [admin['id'] for admin in admins_collection.find({}, {"_id": 0, "id": 1})]  # Replace "id" with the correct field
combined_admins = list(set(ADMINS) | set(db_admins))  # Convert to list to ensure compatibility


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