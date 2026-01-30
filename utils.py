import time
import asyncio
import random
from aiogram import Bot

last_activity = time.time()
last_ping_time = 0

IDLE_VOICES = [
    "AwACAgUAAxkDAAMVaXtSMhAi0AkPeNtl1_29o6LW1QsAAgUZAAJ0XdlXahpPgBCFCv84BA",
    "AwACAgUAAxkDAAMZaXuCNKMRh4UO-0FVBckMH1wXkMsAAggcAAJ0XeFXFyiFt_fmHoQ4BA",
    "AwACAgUAAxkDAAMcaXuCW_T4KzeM64pQjbVvMLDZNoIAAgocAAJ0XeFXuJjDLRdo1l84BA",
    "AwACAgUAAxkDAAMlaXuC4Q49sTjT1SqyUGim01Q3BJ8AAhAcAAJ0XeFXKr5ZIb31tGo4BA"
]

IDLE_TEXT = "Я подключен к нашей таблице, если не прослушаешь поставлю -250 штраф автоматом!"


def update_activity():
    global last_activity
    last_activity = time.time()


async def start_silence_watcher(bot: Bot, chat_id: int):
    global last_ping_time, last_activity

    INTERVAL = 1800
    DELETE_DELAY = 120

    while True:
        await asyncio.sleep(60)

        now = time.time()

        # чат активен
        if now - last_activity < INTERVAL:
            continue

        # антифлуд
        if now - last_ping_time < INTERVAL:
            continue

        try:
            voice_id = random.choice(IDLE_VOICES)  # список плейсхолдеров

            v = await bot.send_voice(chat_id, voice_id)
            t = await bot.send_message(
                chat_id,
                "Я подключен к нашей таблице, если не прослушаешь поставлю -250 штраф автоматом!"
            )

            last_ping_time = now
            last_activity = now

            # async cleanup
            asyncio.create_task(cleanup_idle(bot, chat_id, v.message_id, t.message_id))

        except Exception as e:
            print("Idle watcher error:", e)
            
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