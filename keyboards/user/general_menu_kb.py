from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def create_general_menu(language: str):
    # Словарь для текстов кнопок на разных языках
    buttons_text = {
        "uz": ["Yuklab olish", "Sozlamalar"],
        "ru": ["Скачать", "Настройки"],
        "en": ["Download", "Settings"]
    }

    # Получаем текст кнопок на нужном языке, если язык не найден, используем английский
    buttons = buttons_text.get(language.lower(), buttons_text["en"])

    # Создаем клавиатуру
    general_menu_kb = ReplyKeyboardBuilder()
    general_menu_kb.add(
        KeyboardButton(text=buttons[0]),
        KeyboardButton(text=buttons[1])
    )
    general_menu_kb.adjust(2)

    return general_menu_kb.as_markup(resize_keyboard=True)


