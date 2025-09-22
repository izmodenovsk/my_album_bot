import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"
CHANNEL_ID = -1001234567890  # сюда вставь id твоего канала

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# обработка фото
@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=f"От {message.from_user.first_name}")
    await message.answer("Фото сохранено в альбом 📸")

# обработка видео
@dp.message_handler(content_types=["video"])
async def handle_video(message: types.Message):
    await bot.send_video(CHANNEL_ID, message.video.file_id, caption=f"От {message.from_user.first_name}")
    await message.answer("Видео сохранено в альбом 🎬")

# старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Открыть альбом", web_app=types.WebAppInfo(url="https://ТВОЙ_GITHUB_PAGES.github.io/album")))
    await message.answer("Привет! Отправляй фото или видео — я сохраню их в альбоме.", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
