from aiogram.utils.keyboard import InlineKeyboardBuilder

async def admin_add_stock_menu():
    # Создаем клавиатуру
    add_stock_menu = InlineKeyboardBuilder()
    add_stock_menu.button(text="Basic banners", callback_data="add_stock_basic_baner")
    add_stock_menu.button(text="Promo", callback_data="add_stock_promo")

    # Настраиваем количество кнопок в рядке
    add_stock_menu.adjust(2)

    return add_stock_menu.as_markup(resize_keyboard=True)
