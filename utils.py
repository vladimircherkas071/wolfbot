            exceptimport time
import asyncio
from aiogram import Bot

last_activity = time.time()
watcher_running = False

def update_activity():
    global last_activity
    last_activity = time.time()

async def start_silence_watcher(bot: Bot, chat_id: int, interval=600):
    global last_activity
    global watcher_running

    # защита от мультизапуска
    if watcher_running:
        print("Silence watcher already running")
        return

    watcher_running = True
    print("Silence watcher started")

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
                except Exception as e:
                    print("Delete failed:", e)

                last_activity = time.time()

            except Exception as e:
                print("Silence watcher error:", e)