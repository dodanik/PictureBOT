from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_data_zip_offer_kb(name, section):
    # Создаем клавиатуру
    change_data_zip_offer = InlineKeyboardBuilder()

    # Создаем кнопки
    change_data_zip_offer.button(text="Save current", callback_data=f"chg_dzip_SV_{section}{name.replace(' ', '_')}")
    change_data_zip_offer.button(text="Change", callback_data=f"chg_dzip_CHG_{section}{name.replace(' ','_')}")
    # Настраиваем количество кнопок в рядке
    change_data_zip_offer.adjust(2)

    return change_data_zip_offer.as_markup(resize_keyboard=True)