from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_data_promo_kb():
    # Создаем клавиатуру
    change_data_promo = InlineKeyboardBuilder()

    # Создаем кнопки
    change_data_promo.button(text="Save current", callback_data="chg_DT_ZIP_SV_")
    change_data_promo.button(text="Change", callback_data="chg_DT_ZIP_CHG_")
    # Настраиваем количество кнопок в рядке
    change_data_promo.adjust(2)

    return change_data_promo.as_markup(resize_keyboard=True)