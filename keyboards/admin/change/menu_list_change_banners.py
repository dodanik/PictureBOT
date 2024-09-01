from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_list_change_banners_kb(data, section):
    # Создаем клавиатуру
    list_change_banners_kb = InlineKeyboardBuilder()

    # Создаем кнопки для каждого ключа в словаре
    for name in data:
        # Определяем текст кнопки
        text = f"{name}"
        # Добавляем кнопку с соответствующим текстом и callback_data
        list_change_banners_kb.button(text=text, callback_data=f"chg_b_list_{section}{name.replace(' ', '_')}")

    # Настраиваем количество кнопок в рядке
    list_change_banners_kb.adjust(2)

    return list_change_banners_kb.as_markup(resize_keyboard=True)