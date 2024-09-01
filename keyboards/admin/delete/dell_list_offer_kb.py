from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_del_list_offer_kb(data, section):
    # Создаем клавиатуру
    del_list_offer = InlineKeyboardBuilder()

    # Создаем кнопки для каждого ключа в словаре
    for name in data:
        # Определяем текст кнопки
        text = f"{name}"
        # Добавляем кнопку с соответствующим текстом и callback_data
        del_list_offer.button(text=text, callback_data=f"remove_{section}{name.replace(' ', '_')}")

    # Настраиваем количество кнопок в рядке
    del_list_offer.adjust(2)

    return del_list_offer.as_markup(resize_keyboard=True)