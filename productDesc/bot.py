import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from main import process_product
from dotenv import load_dotenv
from db import log_request

load_dotenv()
# Вставь сюда свой токен или используй переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём объекты
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Пришли фото товара + название и модель (через ;).")

# Фото
@dp.message(lambda msg: msg.photo)
async def handle_photo(message: Message):
    if not message.caption:
        await message.answer("Добавь подпись к фото в формате: Модель; Название")
        return

    # Скачиваем фото
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)

    img_name = "temp.jpg"
    with open(img_name, "wb") as f:
        f.write(downloaded_file.read())

    # Разбираем caption
    parts = message.caption.split(";")
    if len(parts) < 2:
        await message.answer("Формат подписи: Модель; Название")
        return

    model, name = parts[0].strip(), parts[1].strip()

    desc, cat = process_product(img_name, model, name)

    await message.answer(f"✅ Описание: {desc}\n📦 Категория: {cat}")

    await log_request(
        user_id=message.from_user.id,
        model=model,
        name=name,
        description=desc,
        category=cat,
        image_path=img_name
    )

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
