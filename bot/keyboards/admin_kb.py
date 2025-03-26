from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить ID"), KeyboardButton(text="➖ Удалить ID")],
        [KeyboardButton(text="📃 Показать все ID")]
    ],
    resize_keyboard=True
)
