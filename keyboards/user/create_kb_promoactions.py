from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_kb_promoactions(data, lang):
    # Создаем клавиатуру
    promoactions = InlineKeyboardBuilder()
    promoactions.button(text="🏷️ Basic banners", callback_data=f"basic_bnrs_{lang}")
    for name in data:
        promoactions.button(text=f"🎁 {name}", callback_data=f"NM_BN_{name.replace(' ', '_')}_{lang}")

    # Настраиваем количество кнопок в рядке.
    promoactions.adjust(2)

    return promoactions.as_markup(resize_keyboard=True)
