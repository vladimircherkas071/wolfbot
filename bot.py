import asyncio
import random
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from phrases import random_meme, random_oracle, random_wolf, HELP_TEXT
from utils import update_activity, start_silence_watcher
from reactions import gif_reaction, text_reaction, photo_reaction, TRIGGER_GIFS, match_voice

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

LUCIFER_STICKER = "CAACAgIAAxkBAAELVXJpeHeplIUQU_DFFJ-8UZD2rSprZAACoU0AAtW8QEtUa-uvqhhMKDgE"
LUCIFER_TEXT = "Призыв принят. Администратор ада уже в пути."

DELETE_DELAY = 120

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

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
    await bot.send_message(message.chat.id, HELP_TEXT)


@dp.message_handler(commands=["пинок"])
async def kick(message: types.Message):
    update_activity()

    if not message.entities:
        await bot.send_message(message.chat.id, "👢 Кого пинать?")
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
        msg = await bot.send_message(message.chat.id, gif_reaction())
        await asyncio.sleep(DELETE_DELAY)
        try:
            await msg.delete()
        except:
            pass

# ---------------- PHOTO ----------------

@dp.message_handler(content_types=ContentType.PHOTO)
async def react_to_photo(message: types.Message):
    if message.from_user.is_bot:
        return

    update_activity()

    if random.random() < 0.65:
        msg = await bot.send_message(message.chat.id, photo_reaction())
        await asyncio.sleep(DELETE_DELAY)
        try:
            await msg.delete()
        except:
            pass

# ---------------- TEXT ----------------

@dp.message_handler(content_types=ContentType.TEXT)
async def react_to_text(message: types.Message):
    if message.from_user.is_bot:
        return

    if message.text.startswith("/"):
        return

    update_activity()

    text = message.text.lower()

    # ---------- VOICE ----------

    voice_id = match_voice(text)

    if voice_id:
        voice_msg = await bot.send_voice(message.chat.id, voice_id)

        await asyncio.sleep(180)

        try:
            await voice_msg.delete()
        except:
            pass

        return

    # ---------- LUCIFER ----------

    if any(x in text for x in ["lucifer","люцифер","люцик","luccifer","люсик","сатана"]):
        gif_msg = await message.reply_sticker(LUCIFER_STICKER)
        comment = await bot.send_message(message.chat.id, LUCIFER_TEXT)

        await asyncio.sleep(DELETE_DELAY)

        try:
            await gif_msg.delete()
            await comment.delete()
        except:
            pass

        return

    # ---------- KEYWORD GIFS ----------

    for trigger, gif_id in TRIGGER_GIFS.items():
        if trigger in text:
            gif_msg = await message.reply_sticker(gif_id)
            
            await asyncio.sleep(DELETE_DELAY)

            try:
                await gif_msg.delete()
            except:
                pass

            return

    # ---------- RANDOM TEXT ----------

    if random.random() < 0.07:
        await bot.send_message(message.chat.id, text_reaction())

# ---------------- START ----------------

async def main():
    print("🐺 OfficeWolf запущен")
    asyncio.create_task(start_silence_watcher(bot, CHAT_ID))
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())