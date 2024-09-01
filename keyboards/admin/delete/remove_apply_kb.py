from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_remove_apply_kb(section):
    # Создаем клавиатуру
    remove_apply = InlineKeyboardBuilder()

    # Создаем кнопки
    remove_apply.button(text="Cancel", callback_data=f"apply_del_cancel_")
    remove_apply.button(text="Apply", callback_data=f"apply_del_{section}")
    # Настраиваем количество кнопок в рядке
    remove_apply.adjust(2)

    return remove_apply.as_markup(resize_keyboard=True)