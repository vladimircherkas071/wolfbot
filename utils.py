import time
import asyncio
from aiogram import Bot

last_activity = time.time()

def update_activity():
    global last_activity
    last_activity = time.time()


async def start_silence_watcher(bot: Bot, chat_id: int, interval=600):
    """
    Каждые interval секунд проверяет активность.
    Если тишина — пишет в чат.
    """

    global last_activity

    while True:
        await asyncio.sleep(interval)

        if time.time() - last_activity > interval:
            await bot.send_message(
                chat_id,
                "⚰️ Чат мёртв.\n🐺 Вы работаете или изображаете занятость?"
            )

            last_activity = time.time()