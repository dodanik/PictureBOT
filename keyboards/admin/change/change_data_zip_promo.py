from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_data_zip_promo_kb(name):
    # Создаем клавиатуру
    change_data_zip_promo = InlineKeyboardBuilder()

    # Создаем кнопки
    change_data_zip_promo.button(text="Save current", callback_data=f"chg_DT_ZIP_SV_{name.replace(' ','_')}")
    change_data_zip_promo.button(text="Change", callback_data=f"chg_DT_ZIP_CHG_{name.replace(' ','_')}")
    # Настраиваем количество кнопок в рядке
    change_data_zip_promo.adjust(2)

    return change_data_zip_promo.as_markup(resize_keyboard=True)
