from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_delete_menu_kb():
    # Создаем клавиатуру
    delete_menu = InlineKeyboardBuilder()

    # Создаем кнопки
    delete_menu.button(text="Basic banners", callback_data="del_basic_")
    delete_menu.button(text="Promo", callback_data="del_promo_")
    # Настраиваем количество кнопок в рядке
    delete_menu.adjust(2)

    return delete_menu.as_markup(resize_keyboard=True)