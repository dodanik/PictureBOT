from aiogram.utils.keyboard import InlineKeyboardBuilder

async def create_toggle_visibility_kb(data, section):
    # Создаем клавиатуру
    kb_settings_user = InlineKeyboardBuilder()

    # Создаем кнопки для каждого ключа в словаре
    for key, visibility in data.items():
        # Определяем текст кнопки в зависимости от значения visibility
        icon = "♻️" if visibility else "💤"
        text = f"{icon} {key} {icon}"
        # Добавляем кнопку с соответствующим текстом и callback_data
        kb_settings_user.button(text=text, callback_data=f"tgg_vsblt_{section}{key.replace(' ', '_')}")

    # Настраиваем количество кнопок в рядке
    kb_settings_user.adjust(2)

    return kb_settings_user.as_markup(resize_keyboard=True)
