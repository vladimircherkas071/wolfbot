# punish_wheel.py

import random
import asyncio
import json
import os
from aiogram import types
from aiogram.utils.exceptions import MessageNotModified, RetryAfter
from config import load_wheel_access

WHEEL_GIF = "wheel.mp4"
RESULT_GIF = "winner.mp4"
STATS_FILE = "wheel_stats.json"

PUNISHMENTS = [
    "Штраф -100",
    "Завтра работать стоя",
    "Штраф -250",
    "250 приседаний за день",
    "Водонос (завтра носишь воду любому по запросу)",
    "Кукарекаешь в центре зала после утреннего брифа",
    "Завтра ебашишь без брейков",
    "Обед 30 минут",
    "500 приседаний за день",
    "А ты фартовый. Крути еще раз!"
]

SPINNER_FRAMES = [
    "🟡⚫️⚫️⚫️⚫️⚫️⚫️⚫️",
    "⚫️🟡⚫️⚫️⚫️⚫️⚫️⚫️",
    "⚫️⚫️🟡⚫️⚫️⚫️⚫️⚫️",
    "⚫️⚫️⚫️🟡⚫️⚫️⚫️⚫️",
    "⚫️⚫️⚫️⚫️🟡⚫️⚫️⚫️",
    "⚫️⚫️⚫️⚫️⚫️🟡⚫️⚫️",
    "⚫️⚫️⚫️⚫️⚫️⚫️🟡⚫️",
    "⚫️⚫️⚫️⚫️⚫️⚫️⚫️🟡",
]


# ---------------- STATS ----------------

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    try:
      with open(STATS_FILE, "r", encoding="utf-8") as f:
          return json.load(f)
    except Exception as e:
      print("[Stats load error]:", e)
      return {}


def save_stats(data):
  try:
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
  except Exception as e:
    print("[Stats save error]:", e)


def add_stat(chat_id, username, punishment):
    stats = load_stats()
    chat = str(chat_id)

    if chat not in stats:
        stats[chat] = {}

    if username not in stats[chat]:
        stats[chat][username] = []

    stats[chat][username].append(punishment)
    save_stats(stats)


# ---------------- CORE ----------------

async def animate_spinner(msg):
    """
    Казино эффект ~10 секунд
    Без flood
    """

    delays = (
        [0.5] * 4 +   # быстро
        [0.8] * 4 +   # средне
        [1.1] * 4     # медленно
    )

    frame_index = 0
    last = None

    for delay in delays:
        frame = SPINNER_FRAMES[frame_index % len(SPINNER_FRAMES)]
        text = f"🎡 Крутим колесо...\n\n{frame}"

        if text != last:
            try:
                await msg.edit_text(text)
                last = text

            except RetryAfter as e:
                await asyncio.sleep(e.timeout)

            except Exception:
                pass

        frame_index += 1
        await asyncio.sleep(delay)

    # финальная пауза
    try:
        await msg.edit_text("🎡 Колесо замедляется...")
    except:
        pass

    await asyncio.sleep(1.3)

def spin_wheel():
    return random.randrange(len(PUNISHMENTS))


async def run_wheel(bot, chat_id, username):
    await bot.send_message(chat_id, f"🎡 {username} участвует в колесе волоеба…")

    await asyncio.sleep(3)
    with open(WHEEL_GIF, "rb") as f:
      await bot.send_animation(chat_id, f)

    spinner_msg = await bot.send_message(chat_id, "Крутим колесо… Страшно?")

    await animate_spinner(spinner_msg)

    while True:
        result = spin_wheel()
        punishment = PUNISHMENTS[result]

        if result == 10:
            await asyncio.sleep(3)
            await animate_spinner(spinner_msg)
            continue

        text = f"💀 {username}\n\nВыпало:\n👉 {punishment}"
        await spinner_msg.edit_text(text)
        #реакция после результата
        try:
          with open(RESULT_GIF, "rb") as f:
            await bot.send_animation(chat_id, f)
        except Exception as e:
          print("Result gif error:", e)

        add_stat(chat_id, username, punishment)
        break


# ---------------- COMMANDS ----------------

async def wheel_command(message: types.Message, bot):
    access = load_wheel_access()

    chat = str(message.chat.id)
    user = message.from_user.id

    if chat not in access:
        await message.reply("⛔️ В этом чате колесо не подключено.")
        return

    if access[chat] != user:
        await message.reply("⛔️ Только администратор этого чата может запускать колесо.")
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.reply("Использование:\n/wheel Slivki")
        return

    username = parts[1]

    await run_wheel(bot, message.chat.id, username)


async def stats_command(message: types.Message):
    stats = load_stats()
    chat = str(message.chat.id)

    if chat not in stats:
        await message.reply("Пока статистики нет.")
        return

    stats = stats[chat]

    text = "📊 Статистика наказаний:\n\n"

    for user, items in stats.items():
        text += f"{user}: {len(items)}\n"
        for i in items[-5:]:
            text += f"  • {i}\n"
        text += "\n"

    await message.reply(text)