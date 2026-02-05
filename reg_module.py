import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from config import TEAMMATES, REG_GIFS, load_wheel_access
import stats


def random_gif():
    return random.choice(REG_GIFS)


def reg_start_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📞 Трубка", callback_data="reg_pipe"),
        InlineKeyboardButton("💰 Деп", callback_data="reg_dep"),
    )
    return kb


def teammates_kb(chat_id, reg_type):
    kb = InlineKeyboardMarkup()
    for name in TEAMMATES.get(str(chat_id), []):
        kb.add(
            InlineKeyboardButton(
                name,
                callback_data=f"reg_user:{reg_type}:{name}"
            )
        )
    return kb


async def cmd_reg(message: types.Message, bot):
  chat = str(message.chat.id)
  if chat not in TEAMMATES:
    await message.reply("Регистрация в этом чате не включена!")
    return
  try:
    await bot.send_animation(
      message.chat.id,
      open(random_gif(), "rb"),
      caption="Что регаем?",
      reply_markup=reg_start_kb()
    )
  except Exception as e:
    await message.reply(f"reg gif error: {e}")


async def reg_callbacks(call: types.CallbackQuery):
    chat_id = call.message.chat.id

    if call.data == "reg_pipe":
        await call.message.edit_reply_markup(
            teammates_kb(chat_id, "pipe")
        )
        return

    if call.data == "reg_dep":
        await call.message.edit_reply_markup(
            teammates_kb(chat_id, "dep")
        )
        return

    if call.data.startswith("reg_user"):
        _, reg_type, name = call.data.split(":")

        stats.add(chat_id, name, reg_type)

        icon = "📞" if reg_type == "pipe" else "💰"

        await call.message.edit_caption(
            f"{icon} Засчитано\n\n👤 {name}",
            reply_markup=None
        )


async def reset_stats_cmd(message: types.Message):
    chat_id = message.chat.id
    access = load_wheel_access()

    if str(chat_id) not in access or access[str(chat_id)] != message.from_user.id:
        await message.reply("⛔️ Только админ колеса.")
        return

    stats.reset_month(chat_id)
    await message.reply("♻️ Статистика текущего месяца сброшена.")