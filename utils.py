import time
import asyncio
from aiogram import Bot

last_activity = time.time()

def update_activity():
    global last_activity
    last_activity = time.time()

async def start_silence_watcher(bot: Bot, chat_id: int, interval=600):
    """
    Анти-тишина.
    Если нет активности interval секунд — пингует чат.
    Сообщение живёт 2 минуты и удаляется.
    """

    global last_activity

    while True:
        await asyncio.sleep(interval)

        if time.time() - last_activity > interval:
            try:
                msg = await bot.send_message(
                    chat_id,
                    "⚰️ Чат мёртв.\n🐺 Вы работаете или изображаете занятость?"
                )

                # живёт 2 минуты
                await asyncio.sleep(120)

                try:
                    await msg.delete()
                except:
                    pass

                last_activity = time.time()

            except Exception as e:
                print("Silence watcher error:", e)