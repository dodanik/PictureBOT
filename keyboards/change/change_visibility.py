from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_visibility_kb(data):
    # Создаем клавиатуру
    kb_settings_user = InlineKeyboardBuilder()
    kb_settings_user.button(text="Visibility", callback_data=f"change_selecting_section_{data}_visibility")
    kb_settings_user.button(text="Banners", callback_data=f"change_selecting_section_{data}_banners")

    # Настраиваем количество кнопок в рядке.
    kb_settings_user.adjust(2)

    return kb_settings_user.as_markup(resize_keyboard=True)