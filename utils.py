import time
import asyncio
import random
from aiogram import Bot

active_chats = set()
last_activity = time.time()
last_ping_time = 0

IDLE_VOICES = [
    "AwACAgUAAxkDAAMVaXtSMhAi0AkPeNtl1_29o6LW1QsAAgUZAAJ0XdlXahpPgBCFCv84BA",
    "AwACAgUAAxkDAAMZaXuCNKMRh4UO-0FVBckMH1wXkMsAAggcAAJ0XeFXFyiFt_fmHoQ4BA",
    "AwACAgUAAxkDAAMcaXuCW_T4KzeM64pQjbVvMLDZNoIAAgocAAJ0XeFXuJjDLRdo1l84BA",
    "AwACAgUAAxkDAAMlaXuC4Q49sTjT1SqyUGim01Q3BJ8AAhAcAAJ0XeFXKr5ZIb31tGo4BA"
]

IDLE_TEXT = "🎯🔥💪Немножко мотивации Вам в ленту ребятушки!!!🍀"


def update_activity(chat_id=None):
    global last_activity
    last_activity = time.time()
    
    if chat_id:
      active_chats.add(chat_id)


async def start_silence_watcher(bot: Bot):
    global last_ping_time

    while True:
        await asyncio.sleep(20)

        if time.time() - last_activity > 300:
            if time.time() - last_ping_time < 300:
                continue

            last_ping_time = time.time()

            for chat in list(active_chats):
                voice = random.choice(IDLE_VOICES)
                msg = await bot.send_voice(chat, voice)

                # автоудаление
                asyncio.create_task(delete_later(bot, chat, msg.message_id))

async def delete_later(bot, chat_id, msg_id, delay=120):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id, msg_id)
    except:
        pass

async def cleanup_idle(bot, chat_id, voice_id, text_id):
    await asyncio.sleep(120)

    try:
        await bot.delete_message(chat_id, voice_id)
    except:
        pass

    try:
        await bot.delete_message(chat_id, text_id)
    except:
        pass