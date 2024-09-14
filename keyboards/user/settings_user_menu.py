from aiogram.utils.keyboard import InlineKeyboardBuilder



async def create_settings_menu(language: str):
    # Словарь с текстами кнопок на разных языках
    buttons_text = {
        "uz": ["💬 Qo'llab-quvvatlash", "🌐 Bot tilini o'zgartirish"],
        "ru": ["💬 Поддержка", "🌐 Изменить язык бота"],
        "en": ["💬 Support", "🌐 Change Bot language"]
    }

    # Получаем текст кнопок на нужном языке, по умолчанию используем английский
    buttons = buttons_text.get(language.lower(), buttons_text["en"])

    # Создаем клавиатуру
    kb_settings_user = InlineKeyboardBuilder()
    kb_settings_user.button(text=buttons[0], url=f"https://t.me/xDoDAN", callback_data="setting_support")
    kb_settings_user.button(text=buttons[1], callback_data="setting_lang")

    # Настраиваем количество кнопок в рядке
    kb_settings_user.adjust(2)

    return kb_settings_user.as_markup(resize_keyboard=True)
