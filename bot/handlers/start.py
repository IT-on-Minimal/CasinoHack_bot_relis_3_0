from aiogram import F, Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from bot.database.dp import SessionLocal
from bot.database.models import User

router = Router()

# Временное хранилище состояния ожидания ID
awaiting_ids = {}

# Клавиатура выбора языка
lang_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Checker ID по базе", callback_data="lang_check")]
    ]
)

# Клавиатуры регистрации
reg_inline_keyboard_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔗 ССЫЛКА ДЛЯ РЕГИСТРАЦИИ", callback_data="reg_link_ru")],
        [InlineKeyboardButton(text="✅ ЗАРЕГИСТРИРОВАЛСЯ", callback_data="registered_ru")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_lang")]
    ]
)

reg_inline_keyboard_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔗 REGISTER LINK", callback_data="reg_link_en")],
        [InlineKeyboardButton(text="✅ I HAVE REGISTERED", callback_data="registered_en")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_lang")]
    ]
)

# Тестовая reply-клавиатура (опционально)
test_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кнопка 1")],
        [KeyboardButton(text="Кнопка 2")]
    ],
    resize_keyboard=True
)

# Клавиатура выбора игр
games_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⛏ MINERS ⛏", callback_data="game_miners"),
         InlineKeyboardButton(text="⚽ GOAL ⚽", callback_data="game_goal")],
        [InlineKeyboardButton(text="✈️ AVIATRIX ✈️", callback_data="game_aviatrix"),
         InlineKeyboardButton(text="🥅 Penalty Shoot-out 🥅", callback_data="game_penalty")],
        [InlineKeyboardButton(text="🎰 ROULETTE 🎰", callback_data="game_roulette")]
    ]
)

# Команда /test_reply
@router.message(F.text == "/test_reply")
async def test_reply_keyboard_handler(message: Message):
    await message.answer("Вот обычная Reply-клавиатура 👇", reply_markup=test_reply_keyboard)

# Универсальная функция отправки стартового текста
async def send_start_text(bot: Bot, target, is_edit: bool = False):
    text = (
        "Добро пожаловать в сигнальный бот CasinoHack🤖\n"
        "Welcome to the CasinoHack signal bot🤖\n\n"
        "Бот создан на базе ChatGPT-4.0🧠\n"
        "This bot is powered by ChatGPT-4.0🧠\n\n"
        "Продолжая, вы соглашаетесь, что информация предоставляется только в ознакомительных целях.\n"
        "By continuing, you agree that all information is for educational purposes only.\n\n"
        "Выберите язык / Choose a language 👇"
    )

    if is_edit:
        await target.edit_text(text=text, reply_markup=lang_inline_keyboard)
    else:
        # Скрываем reply-клавиатуру и показываем только инлайн-кнопки
        await bot.send_message(
            chat_id=target,
            text=text,
            reply_markup=lang_inline_keyboard
        )


# /start
@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot):
    await send_start_text(bot=bot, target=message.chat.id, is_edit=False)

    session = SessionLocal()
    user_exists = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user_exists:
        new_user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            lang=None
        )
        session.add(new_user)
        session.commit()
    session.close()

# Назад к выбору языка
@router.callback_query(F.data == "back_to_lang")
async def back_to_language(callback: CallbackQuery, bot: Bot):
    await send_start_text(bot=bot, target=callback.message, is_edit=True)
    await callback.answer()

# Выбор языка RU
@router.callback_query(F.data == "lang_ru")
async def lang_ru_selected(callback: CallbackQuery):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    if user:
        user.lang = "ru"
        session.commit()
    session.close()

    await callback.message.edit_text(
        "Бот работает только с новыми аккаунтами, созданными по ссылке.\n\n"
        "Чтобы получить доступ, зарегистрируйтесь по ссылке и отправьте ID нового аккаунта (только цифры).\n\n"
        "Ссылка для регистрации 👇",
        reply_markup=reg_inline_keyboard_ru
    )
    await callback.answer()

# Выбор языка EN
@router.callback_query(F.data == "lang_en")
async def lang_en_selected(callback: CallbackQuery):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    if user:
        user.lang = "en"
        session.commit()
    session.close()

    await callback.message.edit_text(
        "This bot works only with newly created accounts registered via the link below.\n\n"
        "Please register a new account and send your ID (numbers only) to the bot.\n\n"
        "Registration link 👇",
        reply_markup=reg_inline_keyboard_en
    )
    await callback.answer()

# Кнопка "Ссылка для регистрации"
@router.callback_query(F.data == "reg_link_ru")
async def send_registration_link(callback: CallbackQuery):
    await callback.message.answer("Вот ссылка для регистрации: https://example.com/your_link")
    await callback.answer()

@router.callback_query(F.data == "reg_link_en")
async def send_registration_link_en(callback: CallbackQuery):
    await callback.message.answer("Here is the registration link: https://example.com/your_link")
    await callback.answer()

# Кнопка "Зарегистрировался"
@router.callback_query(F.data == "registered_ru")
async def registered_ru(callback: CallbackQuery):
    awaiting_ids[callback.from_user.id] = True
    await callback.message.answer("Введите ID нового аккаунта (только цифры)")
    await callback.answer()

@router.callback_query(F.data == "registered_en")
async def registered_en(callback: CallbackQuery):
    awaiting_ids[callback.from_user.id] = True
    await callback.message.answer("Enter the ID of your new account (numbers only)")
    await callback.answer()

# Обработка ввода ID
@router.message()
async def check_user_id(message: Message):
    if not awaiting_ids.get(message.from_user.id):
        return

    if not message.text.isdigit():
        await message.answer("❌ Ошибка: введите только цифры.")
        return

    user_id = message.text.strip()

    try:
        with open("bot/database/valid_ids.txt", "r", encoding="utf-8") as f:
            valid_ids = f.read().splitlines()
    except FileNotFoundError:
        await message.answer("⚠️ Ошибка: файл с ID не найден.")
        return

    if user_id in valid_ids:
        await message.answer("🔍 Проверяю ID в базе...")
        await message.answer(
            "✅ Доступ открыт!\n\n📋 Инструкция:\n1️⃣ Выберите игру ниже\n2️⃣ Запустите её на сайте\n3️⃣ Повторите сигнал 🎯",
            reply_markup=games_keyboard
        )
        # Удаляем флаг ожидания ID
        awaiting_ids.pop(message.from_user.id, None)
    else:
        await message.answer("❌ ID не найден в базе. Попробуйте снова.")
        # Не удаляем флаг — продолжаем ждать корректный ID

# Обработка выбора игры
@router.callback_query(F.data.startswith("game_"))
async def game_selected(callback: CallbackQuery):
    game = callback.data.replace("game_", "").upper()
    await callback.message.answer(f"🎮 Вы выбрали игру: {game}")
    await callback.answer()
