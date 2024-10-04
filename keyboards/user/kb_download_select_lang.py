from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_download_lang_menu():
    # Создаем клавиатуру
    kb_settings_user = InlineKeyboardBuilder()
    kb_settings_user.button(text="🇷🇺 RU", callback_data="dw_lang_ru")
    kb_settings_user.button(text="🇬🇧 EN", callback_data="dw_lang_en")
    kb_settings_user.button(text="🇺🇿 UZ", callback_data="dw_lang_uz")
    kb_settings_user.button(text="🇰🇿 KZ", callback_data="dw_lang_kz")
    kb_settings_user.button(text="🇦🇿 AZ", callback_data="dw_lang_az")
    kb_settings_user.button(text="🇹🇷 TR", callback_data="dw_lang_tr")
    kb_settings_user.button(text="🇧🇷 BR", callback_data="dw_lang_br")
    kb_settings_user.button(text="🇵🇰 UR", callback_data="dw_lang_ur")


    # Настраиваем количество кнопок в рядке
    kb_settings_user.adjust(2, 2, 2, 2)

    return kb_settings_user.as_markup(resize_keyboard=True)
