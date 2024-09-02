from aiogram.utils.keyboard import InlineKeyboardBuilder


# Словарь с переводами для разных языков
translations = {
    'ru': {
        'add_promo_code': "Добавить промокод",
        'without_promo_code': "Без промокода"
    },
    'en': {
        'add_promo_code': "Add promo code",
        'without_promo_code': "Without promo code"
    },
    'uz': {
        'add_promo_code': "Promo kod qo'shish",
        'without_promo_code': "Promo kodsiz"
    }
}

async def create_promo_code_confirm_kb(name, lang, langKb):
    # Создаем клавиатуру
    promo_code_confirm = InlineKeyboardBuilder()

    # Получаем переводы для выбранного языка
    texts = translations.get(langKb, translations['en'])  # По умолчанию используется английский

    # Добавляем кнопки с переводами
    promo_code_confirm.button(text=texts['add_promo_code'], callback_data=f"dwnl_promo_{name}_{lang}")
    promo_code_confirm.button(text=texts['without_promo_code'], callback_data=f"dwnl_no_{name}_{lang}")

    # Настраиваем количество кнопок в рядке.
    promo_code_confirm.adjust(2)

    return promo_code_confirm.as_markup(resize_keyboard=True)