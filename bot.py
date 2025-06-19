import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from db import init_db, add_user, get_progress

# Инициализация бота с parse_mode через DefaultBotProperties
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

# Клавиатура с кнопкой "Мой прогресс"
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Мой прогресс")]],
    resize_keyboard=True
)

@dp.message(F.text.startswith("/start"))
async def start_handler(message: types.Message):
    args = message.text.split(" ")[1:]  # Параметры из ссылки (если есть)
    user_id = message.from_user.id

    # Определяем, кто пригласил (если есть)
    ref_by = int(args[0]) if args and args[0].isdigit() and int(args[0]) != user_id else None
    await add_user(user_id, ref_by)

    ref_count = await get_progress(user_id)

    if ref_count < 5:
        await message.answer(
            f"👋 <b>Добро пожаловать LEKOMODA !</b>\n\n"
            f"📚 Чтобы получить бесплатные уроки, пожалуйста, пригласите 5 своих друзей 👥 .\n\n"
            f"<b>Переотправьте это сообщение своим друзьям 📎  :</b>\n"
            f"https://t.me/lekomodabot?start={user_id}\n\n"
            f"<b>Что нужно сделать:</b>\n"
            f"1. Это ваша личная ссылка\n"
            f"2. Отправьте её своим друзьям\n"
            f"3. Когда 5 человек нажмут “Старт ▶️ ” по вашей ссылке — доступ откроется!\n\n"
            f"Вы пригласили <b>{ref_count}</b> из 5 друзей 👥 .\n\n" 

            "<b>📚 Основные разделы бесплатных уроков:</b>\n"
            "• Введение в цифровое моделирование одежды\n"
            "• Простые проекты для самостоятельной практики\n"
            "• Советы по выбору программного обеспечения и оборудования\n\n"
            "<b>💡 Дополнительные возможности платных курсов:</b>\n"
            "• Расширенные теоретические модули и пошаговые видеоуроки\n"
            "• Практические задания с обратной связью от преподавателя\n"
            "• Доступ к закрытому чату для общения и поддержки\n"
            "• Персональные консультации и проверка домашних заданий\n\n"
            "<a href='https://leko-moda.com/'>👉 Перейти на сайт ❤️ Lekomoda</a>",
            reply_markup=keyboard
        )
    else:
        await send_access_message(message)

@dp.message(F.text.in_({"Мой прогресс", "/progress"}))
async def progress_handler(message: types.Message):
    count = await get_progress(message.from_user.id)
    if count < 5:
        await message.answer(f"📊 Вы пригласили <b>{count}</b> из 5 друзей. Продолжайте!", reply_markup=keyboard)
    else:
        await send_access_message(message)

async def send_access_message(message: types.Message):
    await message.answer(
        "🎉 <b>Отлично! Вы пригласили 5 друзей.</b>\n"
        "Теперь вам открыт полный доступ к урокам и материалам!\n\n"
        "<b>📚 Основные разделы бесплатных уроков:</b>\n"
        "• Введение в цифровое моделирование одежды\n"
        "• Простые проекты для самостоятельной практики\n"
        "• Советы по выбору программного обеспечения и оборудования\n\n"
        "<b>💡 Дополнительные возможности платных курсов:</b>\n"
        "• Расширенные теоретические модули и пошаговые видеоуроки\n"
        "• Практические задания с обратной связью от преподавателя\n"
        "• Доступ к закрытому чату для общения и поддержки\n"
        "• Персональные консультации и проверка домашних заданий\n\n"
        "<a href='https://leko-moda.com/'>👉 Перейти на сайт ❤️ Lekomoda</a>"
    )

async def main():
    await init_db()
    # Не нужно include_router(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
