import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo
import os

API_TOKEN = os.getenv("BOT_TOKEN", "ТОКЕН_ТВОЕГО_БОТА")
CHANNEL_ID = -1001234567890  # замени на id твоего канала

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Храним ссылки на файлы в памяти (позже можно сделать базу)
album = []


# обработка фото
@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    album.append({"type": "photo", "file_id": file_id})
    await bot.send_photo(CHANNEL_ID, file_id, caption=f"От {message.from_user.first_name}")
    await message.answer("Фото сохранено в альбом 📸")


# обработка видео
@dp.message_handler(content_types=["video"])
async def handle_video(message: types.Message):
    file_id = message.video.file_id
    album.append({"type": "video", "file_id": file_id})
    await bot.send_video(CHANNEL_ID, file_id, caption=f"От {message.from_user.first_name}")
    await message.answer("Видео сохранено в альбом 🎬")


# команда /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Открыть альбом", web_app=WebAppInfo(url="https://USERNAME.github.io/my_album_bot/album")))
    await message.answer("Привет! Отправляй фото или видео — я сохраню их в альбоме.", reply_markup=kb)


# выдача JSON со списком файлов
@dp.message_handler(commands=["album"])
async def get_album(message: types.Message):
    if not album:
        await message.answer("Альбом пока пуст 📭")
        return

    # строим JSON вручную
    json_data = "[\n"
    for item in album:
        if item["type"] == "photo":
            file = await bot.get_file(item["file_id"])
            file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"
            json_data += f'  {{"type": "photo", "url": "{file_url}"}},\n'
        elif item["type"] == "video":
            file = await bot.get_file(item["file_id"])
            file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"
            json_data += f'  {{"type": "video", "url": "{file_url}"}},\n'
    json_data = json_data.rstrip(",\n") + "\n]"

    await message.answer(f"<pre>{json_data}</pre>", parse_mode="HTML")
