import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from config import TEAMMATES, REG_GIFS, WHEEL_ADMINS
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
    for name in TEAMMATES.get(chat_id, []):
        kb.add(
            InlineKeyboardButton(
                name,
                callback_data=f"reg_user:{reg_type}:{name}"
            )
        )
    return kb


async def cmd_reg(message: types.Message, bot):
    if message.chat.id not in TEAMMATES:
        return

    await bot.send_animation(
        message.chat.id,
        open(random_gif(), "rb"),
        caption="Что регаем?",
        reply_markup=reg_start_kb()
    )


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

    if WHEEL_ADMINS.get(chat_id) != message.from_user.id:
        await message.reply("⛔️ Только админ колеса.")
        return

    stats.reset_month(chat_id)
    await message.reply("♻️ Статистика текущего месяца сброшена.")