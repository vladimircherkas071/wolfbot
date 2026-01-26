from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType
import random

from phrases import random_meme, random_oracle, random_wolf, HELP_TEXT
from utils import update_activity, start_silence_watcher
from fun.reactions import gif_reaction, text_reaction, photo_reaction

import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# ---------- КОМАНДЫ ----------

@dp.message_handler(content_types=["animation"])
async def catch_gif(message: types.Message):
    print(message.animation.file_id)

@dp.message_handler(commands=["мем"])
async def meme(message: types.Message):
    update_activity()
    await message.reply(random_meme())

@dp.message_handler(commands=["оракул"])
async def oracle(message: types.Message):
    update_activity()
    await message.reply(random_oracle())

@dp.message_handler(commands=["волк"])
async def wolf(message: types.Message):
    update_activity()
    await message.reply(random_wolf())

@dp.message_handler(commands=["help", "помощь", "инструкция"])
async def help_command(message: types.Message):
    update_activity()
    await message.reply(HELP_TEXT)

@dp.message_handler(commands=["пинок"])
async def kick(message: types.Message):
    update_activity()
    if not message.entities:
        await message.reply("👢 Кого пинать? Сам себя?")
        return

    for ent in message.entities:
        if ent.type == "mention":
            user = ent.get_text(message.text)
            await message.reply(
                f"👢 {user} получил пинок.\n"
                f"📉 Активность не обнаружена.\n"
                f"🐺 Соберись."
            )

# ---------- GIF / СТИКЕРЫ / ВИДЕО-ГИФ ----------

@dp.message_handler(
    content_types=[
        ContentType.ANIMATION,
        ContentType.STICKER,
        ContentType.DOCUMENT
    ]
)
async def react_to_gif(message: types.Message):
    if message.from_user.is_bot:
        return

    # document — только gif/mp4
    if message.document:
        if message.document.mime_type not in ("video/mp4", "image/gif"):
            return

    update_activity()
    print("GIF / STICKER пойман")
    
    if random.random() < 0.4:
      await message.reply(gif_reaction())
    else:
      print("Gif пойман, но бот молчит по вероятности")

# ---------- ФОТО ----------

@dp.message_handler(content_types=ContentType.PHOTO)
async def react_to_photo(message: types.Message):
    if message.from_user.is_bot:
        return

    update_activity()
    print("PHOTO пойман")
    
    if random.random() < 0.65:
      await message.reply(photo_reaction())
    else:
      print("фото поймано, но бот молчит по вероятности")

# ---------- ТЕКСТ ----------

@dp.message_handler(content_types=ContentType.TEXT)
async def react_to_text(message: types.Message):
    if message.from_user.is_bot:
        return

    if message.text.startswith("/"):
        return

    update_activity()

    # шанс реакции 7%
    if random.random() < 0.07:
        await message.reply(text_reaction())

# ---------- СТАРТ ----------

if __name__ == "__main__":
    print("🐺 OfficeWolf запущен")
    start_silence_watcher(bot, CHAT_ID)
    executor.start_polling(dp, skip_updates=True)