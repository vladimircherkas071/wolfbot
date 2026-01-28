import time
import asyncio
from aiogram import Bot

last_activity = time.time()
last_ping_time = 0


def update_activity():
    global last_activity
    last_activity = time.time()


async def start_silence_watcher(bot: Bot, chat_id: int, interval=1800):
    """
    Анти-тишина с защитой от спама + автоудаление пинга
    """

    global last_ping_time, last_activity

    while True:
        await asyncio.sleep(interval)

        now = time.time()

        # если чат активен — ничего не делаем
        if now - last_activity < interval:
            continue

        # защита от флуда (не чаще чем раз в 30 минут)
        if now - last_ping_time < 1800:
            continue

        try:
            msg = await bot.send_message(
                chat_id,
                "⚰️ Чат мёртв.\n🐺 Вы работаете или изображаете занятость?"
            )

            last_ping_time = now
            last_activity = now

            # автоудаление через 2 минуты
            await asyncio.sleep(120)

            try:
                await msg.delete()
            except:
                pass

        except Exception as e:
            print("Silence watcher error:", e)