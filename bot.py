import asyncio
import random
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from phrases import random_meme, random_oracle, random_wolf, HELP_TEXT
from utils import update_activity, start_silence_watcher
from fun.reactions import gif_reaction, text_reaction, photo_reaction

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

LUCIFER_STICKER = "CAACAgIAAxkBAAELVXJpeHeplIUQU_DFFJ-8UZD2rSprZAACoU0AAtW8QEtUa-uvqhhMKDgE"
LUCIFER_TEXT = "Призыв принят. Администратор ада уже в пути."

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# ---------------- CLEANUP ----------------

async def cleanup_lucifer():
    try:
        async for msg in bot.get_chat_history(CHAT_ID, limit=50):
            try:
                if msg.sticker and msg.sticker.file_id == LUCIFER_STICKER:
                    await msg.delete()

                if msg.text == LUCIFER_TEXT:
                    await msg.delete()
            except:
                pass
    except:
        pass

# ---------------- COMMANDS ----------------

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

# ---------------- GIF / STICKER ----------------

@dp.message_handler(content_types=[ContentType.ANIMATION, ContentType.STICKER, ContentType.DOCUMENT])
async def react_to_gif(message: types.Message):
    if message.from_user.is_bot:
        return

    if message.document:
        if message.document.mime_type not in ("video/mp4", "image/gif"):
            return

    update_activity()

    if random.random() < 0.4:
        await message.reply(gif_reaction())

# ---------------- PHOTO ----------------

@dp.message_handler(content_types=ContentType.PHOTO)
async def react_to_photo(message: types.Message):
    if message.from_user.is_bot:
        return

    update_activity()

    if random.random() < 0.65:
        await message.reply(photo_reaction())

# ---------------- TEXT + LUCIFER ----------------

@dp.message_handler(content_types=ContentType.TEXT)
async def react_to_text(message: types.Message):
    if message.from_user.is_bot:
        return

    if message.text.startswith("/"):
        return

    update_activity()

    text = message.text.lower()

    # ---- LUCIFER ----
    if "lucifer" in text or "люцифер" in text or "люцик" in text or "luccifer" in text or "люсик" in text or "сатана" in text:

        gif_msg = await message.reply_sticker(LUCIFER_STICKER)
        comment_msg = await message.reply(LUCIFER_TEXT)

        await asyncio.sleep(120)

        try:
            await gif_msg.delete()
            await comment_msg.delete()
        except:
            pass

        return

    # ---- RANDOM TEXT ----
    if random.random() < 0.07:
        await message.reply(text_reaction())

# ---------------- START ----------------

async def main():
    print("🐺 OfficeWolf запущен")

    await cleanup_lucifer()

    asyncio.create_task(start_silence_watcher(bot, CHAT_ID))

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())