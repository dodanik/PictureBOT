from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters.chat_type_filter import get_my_admins_list


async def create_general_menu(language: str, user_id=False):

    admin_list = await get_my_admins_list()
    if user_id not in admin_list:
        # Словарь для текстов кнопок на разных языках
        buttons_text = {
            "uz": ["📥 Yuklab olish", "🛠️ Sozlamalar"],
            "ru": ["📥 Скачать", "🛠️ Настройки"],
            "en": ["📥 Download", "🛠️ Settings"]
        }

        # Получаем текст кнопок на нужном языке, если язык не найден, используем английский
        buttons = buttons_text.get(language.lower(), buttons_text["en"])

        # Создаем клавиатуру
        general_menu_kb = ReplyKeyboardBuilder()
        general_menu_kb.add(
            KeyboardButton(text=buttons[0]),
            KeyboardButton(text=buttons[1]),
            KeyboardButton(text="⁉️ FAQ")

        )
        general_menu_kb.adjust(2, 1)

        return general_menu_kb.as_markup(resize_keyboard=True)
    else:
        general_menu_admins_kb = ReplyKeyboardBuilder()
        general_menu_admins_kb.add(
            KeyboardButton(text='📥 Download'),
            KeyboardButton(text='Upload'),
            KeyboardButton(text='Settings')
        )
        general_menu_admins_kb.adjust(2, 1)
        return general_menu_admins_kb.as_markup(resize_keyboard=True)


