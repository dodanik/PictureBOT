from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_language_keyboard() -> InlineKeyboardMarkup:
    # Створюємо об'єкт InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()

    # Додаємо кнопки до клавіатури
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇺🇸 English", callback_data="lang_en")
    builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")

    # Додаємо кнопки у рядки
    builder.adjust(2, 1)  # Перший рядок

    # Створюємо об'єкт InlineKeyboardMarkup
    keyboard = builder.as_markup()
    return keyboard