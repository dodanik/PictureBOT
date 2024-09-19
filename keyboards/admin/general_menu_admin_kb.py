from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

general_menu_admins_kb = ReplyKeyboardBuilder()
general_menu_admins_kb.add(
    KeyboardButton(text='📥 Download'),
    KeyboardButton(text='Upload'),
    KeyboardButton(text='Settings')
)
general_menu_admins_kb.adjust(2, 1)
