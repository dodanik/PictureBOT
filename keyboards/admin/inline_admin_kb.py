from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb_upload = InlineKeyboardBuilder()
# Додаємо кнопки до клавіатури
kb_upload.button(text="Add", callback_data="action_add")
kb_upload.button(text="Change", callback_data="action_change")
kb_upload.button(text="Delete", callback_data="action_delete")


# Додаємо кнопки у рядки
kb_upload.adjust(2, 1)  # Перший рядок







