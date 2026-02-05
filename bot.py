import asyncio
import random
import os
import traceback

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from phrases import random_meme, random_oracle, random_wolf, HELP_TEXT
from utils import update_activity, start_silence_watcher
from fun.reactions import (
    gif_reaction,
    text_reaction,
    photo_reaction,
    TRIGGER_GIFS,
    match_voice,
    match_lucifer,
)

from punish_wheel import wheel_command, stats_command

from reg_module import cmd_reg, reg_callbacks, reset_stats_cmd
import stats


TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

DELETE_DELAY = 120

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def cleanup(chat_id, trigger_id, bot_id):
    await asyncio.sleep(DELETE_DELAY)
    try:
        if trigger_id:
            await bot.delete_message(chat_id, trigger_id)
        await bot.delete_message(chat_id, bot_id)
    except:
        pass

# ---------- COMMANDS ----------

@dp.message_handler(commands=["мем"])
async def meme(message: types.Message):
    update_activity(message.chat.id)
    await message.reply(random_meme())


@dp.message_handler(commands=["оракул"])
async def oracle(message: types.Message):
    update_activity(message.chat.id)
    await message.reply(random_oracle())


@dp.message_handler(commands=["волк"])
async def wolf(message: types.Message):
    update_activity(message.chat.id)
    await message.reply(random_wolf())

#---------- WHEEL ----------

@dp.message_handler(commands=["wheel"])
async def wheel(msg: types.Message):
  await wheel_command(msg, bot)
  
@dp.message_handler(commands=["wheel_stats"])
async def wheel_stats(msg: types.Message):
  await stats_command(msg)


@dp.message_handler(commands=["help", "помощь", "инструкция"])
async def help_command(message: types.Message):
    update_activity(message.chat.id)
    await bot.send_message(message.chat.id, HELP_TEXT)

#---------- REGISTRATION ----------

@dp.message_handler(commands=["reg"])
async def reg(message: types.Message):
  #print("REG COMMAND FIRED")
  await cmd_reg(message, bot)

@dp.message_handler(commands=["stats"])
async def reg_stats(message: types.Message):
    text = stats.format_stats(message.chat.id)
    await message.reply(text)

@dp.message_handler(commands=["reset_stats"])
async def reset_stats(message: types.Message):
    await reset_stats_cmd(message)


@dp.callback_query_handler(lambda c: c.data.startswith("reg"))
async def reg_cb(call: types.CallbackQuery):
    await reg_callbacks(call)

# ---------- MEDIA ----------

@dp.message_handler(content_types=ContentType.VOICE)
async def catch_voice(message: types.Message):
    print("VOICE ID:", message.voice.file_id)


@dp.message_handler(content_types=[ContentType.ANIMATION, ContentType.STICKER, ContentType.DOCUMENT])
async def react_media(message: types.Message):
    try:
        update_activity(message.chat.id)

        if random.random() < 0.4:
            msg = await bot.send_message(message.chat.id, gif_reaction())
            asyncio.create_task(cleanup(message.chat.id, None, msg.message_id))

    except:
        traceback.print_exc()


@dp.message_handler(content_types=ContentType.PHOTO)
async def react_photo(message: types.Message):
    try:
        update_activity(message.chat.id)

        if random.random() < 0.65:
            msg = await bot.send_message(message.chat.id, photo_reaction())
            asyncio.create_task(cleanup(message.chat.id, None, msg.message_id))

    except:
        traceback.print_exc()


# ---------- TEXT ----------

@dp.message_handler(content_types=ContentType.TEXT)
async def react_text(message: types.Message):
    try:
        if message.from_user.is_bot:
            return

        if message.text.startswith("/"):
            return

        update_activity(message.chat.id)

        text = message.text.lower()

        # voice reactions
        voice_id = match_voice(text)
        if voice_id:
            v = await bot.send_voice(message.chat.id, voice_id)
            asyncio.create_task(cleanup(message.chat.id, message.message_id, v.message_id))
            return

        # lucifer
        lucifer = match_lucifer(text)
        if lucifer:
            s, m = lucifer
            st = await message.reply_sticker(s)
            msg = await bot.send_message(message.chat.id, m)
            asyncio.create_task(cleanup(message.chat.id, message.message_id, msg.message_id))
            asyncio.create_task(cleanup(message.chat.id, None, st.message_id))
            return

        # gif triggers
        for trigger, gif_id in TRIGGER_GIFS.items():
            if trigger in text:
                g = await message.reply_sticker(gif_id)
                asyncio.create_task(cleanup(message.chat.id, message.message_id, g.message_id))
                return

        # random text
        if random.random() < 0.07:
            m = await bot.send_message(message.chat.id, text_reaction())
            asyncio.create_task(cleanup(message.chat.id, None, m.message_id))

    except:
        traceback.print_exc()

# ---------- START ----------

async def main():
    asyncio.create_task(start_silence_watcher(bot))
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())