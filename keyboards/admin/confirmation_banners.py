from aiogram.utils.keyboard import InlineKeyboardBuilder


async def confirmation_banners_kb():
    # Создаем клавиатуру
    confirmation_banners = InlineKeyboardBuilder()
    confirmation_banners.button(text="Remake", callback_data="confirmation_banners_remake")
    confirmation_banners.button(text="Apply", callback_data="confirmation_banners_apply")

    # Настраиваем количество кнопок в рядке
    confirmation_banners.adjust(2)

    return confirmation_banners.as_markup(resize_keyboard=True)
