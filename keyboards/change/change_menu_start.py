from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_kb_chang():
    # Создаем клавиатуру
    kb_chang = InlineKeyboardBuilder()
    kb_chang.button(text="Basic banners", callback_data="change_start_basic_banners")
    kb_chang.button(text="Promo", callback_data="change_start_promo")

    # Настраиваем количество кнопок в рядке.
    kb_chang.adjust(2)

    return kb_chang.as_markup(resize_keyboard=True)