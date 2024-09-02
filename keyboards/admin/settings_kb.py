from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_kb_change_admin():
    # Создаем клавиатуру
    promoactions = InlineKeyboardBuilder()
    promoactions.button(text="ADD Admin", callback_data="select_admin_add_admin")
    promoactions.button(text="DEL Admin", callback_data="select_admin_del_admin")


    # Настраиваем количество кнопок в рядке.
    promoactions.adjust(2)

    return promoactions.as_markup(resize_keyboard=True)