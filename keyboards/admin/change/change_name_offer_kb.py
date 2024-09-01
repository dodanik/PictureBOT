from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_name_offer_kb(name, section):
    # Создаем клавиатуру
    change_name_offer = InlineKeyboardBuilder()

    # Создаем кнопки
    change_name_offer.button(text="Save current", callback_data=f"chg_NM_SV_{section}{name.replace(' ','_')}")
    change_name_offer.button(text="Change", callback_data=f"chg_NM_CHG_{section}{name.replace(' ','_')}")
    # Настраиваем количество кнопок в рядке
    change_name_offer.adjust(2)

    return change_name_offer.as_markup(resize_keyboard=True)
