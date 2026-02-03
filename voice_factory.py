import os
import asyncio
import subprocess

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN") or "8508519809:AAFgIb3qNhW0-gMseeneZ_F_Doj9uSy5Heg"
OWNER_ID = "8334582417"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

TMP_DIR = "./voices"

os.makedirs(TMP_DIR, exist_ok=True)

print("🐺 VoiceFactory started")


def convert_to_ogg(src, dst):
    print("FFMPEG CONVERT")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", src,
        "-vn",
        "-acodec", "libopus",
        "-b:a", "24k",
        dst
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def handle_mp3(message: types.Message):

    if message.from_user.id != OWNER_ID:
        return

    print("MP3 получил, ща все сделаем быстро!")

    file = await bot.get_file(message.audio.file_id)

    src = f"{TMP_DIR}/{message.audio.file_unique_id}.mp3"
    dst = f"{TMP_DIR}/{message.audio.file_unique_id}.ogg"

    await bot.download_file(file.file_path, src)

    print("ЗАГРУЖЕНО:", src)

    convert_to_ogg(src, dst)

    print("КОНВЕРТИРОВАНО:", dst)

    voice = await bot.send_voice(
        chat_id=OWNER_ID,
        voice=types.InputFile(dst)
    )

    vid = voice.voice.file_id

    print("\n======= VOICE ID =======")
    print(vid)
    print("=======================\n")

    await message.reply(f"🎧 VOICE ID:\n\n{vid}")

    os.remove(src)
    os.remove(dst)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)