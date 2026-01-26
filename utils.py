import time
from threading import Thread
from aiogram import Bot

last_activity = time.time()

def update_activity():
    global last_activity
    last_activity = time.time()

def start_silence_watcher(bot: Bot, chat_id: int, interval=600):
    """
    Авто-анти-тишина. Каждые interval секунд проверяет активность.
    Если нет сообщений — шлёт предупреждение.
    """
    def watcher():
        global last_activity
        while True:
            time.sleep(interval)
            if time.time() - last_activity > interval:
                bot.send_message(chat_id, 
                    "⚰️ Чат мёртв.\n🐺 Вы работаете или изображаете занятость?")
                last_activity = time.time()
    Thread(target=watcher, daemon=True).start()