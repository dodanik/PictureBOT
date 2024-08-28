from aiogram.utils.keyboard import InlineKeyboardBuilder

async def confirmation_promocode_kb():
    # Создаем клавиатуру
    confirmation_promocode = InlineKeyboardBuilder()
    confirmation_promocode.button(text="Promo ❌", callback_data="set_promo_false")
    confirmation_promocode.button(text="Promo ✅", callback_data="set_promo_true")

    # Настраиваем количество кнопок в рядке
    confirmation_promocode.adjust(2)

    return confirmation_promocode.as_markup(resize_keyboard=True)