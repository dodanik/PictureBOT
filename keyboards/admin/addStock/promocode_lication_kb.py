from aiogram.utils.keyboard import InlineKeyboardBuilder


async def location_promocode_kb(selected: str = None):
    # Создаем клавиатуру
    location_promocode = InlineKeyboardBuilder()

    # Кнопки
    buttons = [
        ("Top center", "location_promocode_Top_center"),
        ("Top bottom", "location_promocode_Top_bottom"),
        ("Bottom left", "location_promocode_Bottom_left")
    ]

    # Добавляем кнопки с возможностью выбора
    for text, callback_data in buttons:
        if selected == text:
            text = f"✅ {text}"
        location_promocode.button(text=text, callback_data=callback_data)



    # Добавляем кнопку подтверждения, если что-то выбрано
    if selected:
        apply_callback_data = f"location_promocode_apply_{selected.replace(' ', '_')}"
        location_promocode.button(text="Apply", callback_data=apply_callback_data)

    # Настраиваем количество кнопок в рядке
    location_promocode.adjust(2, 1, 1)

    return location_promocode.as_markup(resize_keyboard=True)