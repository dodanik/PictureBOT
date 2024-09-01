from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_change_location_promocode_kb():
    # Создаем клавиатуру
    change_location_promocode = InlineKeyboardBuilder()

    # Создаем кнопки
    change_location_promocode.button(text="Save current", callback_data="chg_LC_PC_SV_")
    change_location_promocode.button(text="Change", callback_data="chg_LC_PC_CHG_")
    # Настраиваем количество кнопок в рядке
    change_location_promocode.adjust(2)

    return change_location_promocode.as_markup(resize_keyboard=True)