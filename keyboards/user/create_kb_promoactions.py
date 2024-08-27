from aiogram.utils.keyboard import InlineKeyboardBuilder

#Времення функция до написания логики автогенеравции по доступным файлам
async def create_kb_promoactions(lang):
    # Создаем клавиатуру
    kb_settings_user = InlineKeyboardBuilder()
    kb_settings_user.button(text="RU_Promotions", callback_data="name_baner_ru")
    kb_settings_user.button(text="EN_promotions", callback_data="name_baner_ru")

    # Настраиваем количество кнопок в рядке.
    kb_settings_user.adjust(2)

    return kb_settings_user.as_markup(resize_keyboard=True)
