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


async def start_silence_watcher(bot: Bot, chat_id: int, interval=1800):
    global last_ping_time, last_activity

    while True:
        await asyncio.sleep(interval)

        now = time.time()

        if now - last_activity < interval:
            continue

        if now - last_ping_time < 1800:
            continue

        try:
            voice = random.choice(IDLE_VOICES)

            v = await bot.send_voice(chat_id, voice)
            t = await bot.send_message(chat_id, IDLE_TEXT)

            last_ping_time = now
            last_activity = now

            await asyncio.sleep(120)

            try:
                await v.delete()
                await t.delete()
            except:
                pass

        except Exception as e:
            print("Silence watcher error:", e)