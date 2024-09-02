async def get_text_message(language, key):
    # Словарь с переводами фраз
    phrases = {
        'ru': {
            'change_key': "Нажмите соответствующую клавишу для изменения",
            'select_language': "Выберите язык для загрузки",
            'select_banners': "Выберите тип баннеров, который вы хотите загрузить. Далее вам будет предложено ввести промокод",
            'add_promo': "Добавить промокод в баннер?",
            'enter_promo_text': "Введите текст промокода:",
            'promo_no_exists': "Эта акция больше не существует.",
            'zip_without_promo': "Ваш zip-архив создан без промокода.",
            'zip_with_promo': "Ваш zip-архив создан с введенным вами промокодом.",
            'enter_correct_promo': "Пожалуйста, введите правильный промокод:"
        },
        'en': {
            'change_key': "Press the corresponding key to change",
            'select_language': "Select language to download",
            'select_banners': "Select the type of banners you would like to download. Next, you will be able to enter promocode",
            'add_promo': "Add promo code to banner?",
            'enter_promo_text': "Enter the promo code text:",
            'promo_no_exists': "This promotion no longer exists.",
            'zip_without_promo': "Your zip archive created without a promotional code.",
            'zip_with_promo': "Your zip archive created with the promotional code you entered.",
            'enter_correct_promo': "Please enter the correct promotional code:"
        },
        'uz': {
            'change_key': "O'zgartirish uchun mos tugmani bosing",
            'select_language': "Yuklab olish uchun tilni tanlang",
            'select_banners': "Yuklab olish uchun bannerlar turini tanlang. Keyin sizga promokod kiriting",
            'add_promo': "Bannerga promokod qo'shasizmi?",
            'enter_promo_text': "Promokod matnini kiriting:",
            'promo_no_exists': "Bu aksiyadan foydalanish muddati tugagan.",
            'zip_without_promo': "Sizning zip arxivingiz promokodsiz yaratildi.",
            'zip_with_promo': "Siz kiritgan promokod bilan zip arxiv yaratildi.",
            'enter_correct_promo': "Iltimos, to'g'ri promokodni kiriting:"
        }
    }
    # Получаем фразу по ключу и языку
    return phrases.get(language, {}).get(key, "Фраза не найдена")