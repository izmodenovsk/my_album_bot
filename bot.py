import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiohttp import web
import asyncio

API_TOKEN = os.getenv("BOT_TOKEN", "ТОКЕН_ТВОЕГО_БОТА")
CHANNEL_ID = -1002365418629  # замени на id твоего канала

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хранилище файлов (в памяти)
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


# кнопка "Открыть альбом"
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Открыть альбом", web_app=WebAppInfo(url="https://izmodenovsk.github.io/my_album_bot/")))
    await message.answer("Привет! Отправляй фото или видео — я сохраню их в альбоме.", reply_markup=kb)


# ==============================
#   API-сервер (aiohttp)
# ==============================
async def handle_album(request):
    results = []
    for item in album:
        file = await bot.get_file(item["file_id"])
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"
        results.append({"type": item["type"], "url": file_url})
    return web.json_response(results)


async def on_startup(app):
    # Запускаем aiogram внутри aiohttp
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())


def create_app():
    app = web.Application()
    app.router.add_get("/album", handle_album)
    app.on_startup.append(on_startup)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
