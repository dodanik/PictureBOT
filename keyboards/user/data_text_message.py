async def get_text_message(language, key):
    # Словарь с переводами фраз
    phrases = {
        'ru': {
            'change_key': "Добро пожаловать в раздел поддержки! 📚\nЗдесь вы можете ознакомиться с разделом FAQ, где собраны самые популярные ответы на вопросы пользователей.\nМы подготовили для вас полезные советы и рекомендации, чтобы вы могли быстро найти нужную информацию и легко решить любые возникшие проблемы.\n \nИзменить язык! 🌐\nВы также можете легко изменить язык бота.\nПросто выберите предпочитаемый язык, и все сообщения будут отображаться на нем.",
            'select_language': "🌍 Выберите язык для загрузки баннеров, и они будут отображаться именно на выбранном вами языке.",
            'select_banners': "Выберите тип баннеров! 🎰\n\nBasic banners 🏷️:\n ❗️ Здесь собраны все основные предложения!\n\nPromo 🎁:\n ❗️ В данном разделе Вы так же можете выбрать и другие актуальные предложения и акции, участие в которых будет давать бонусы или фрибеты.\n\nДалее, если вы выберете опцию с промокодами, получите баннеры, которые активируют дополнительные скидки.\nЕсли же выберете без промокода, вас ждет архив с актуальными предложениями, без промокода.",
            'add_promo': "С промокодом ✨:\n ♦️ Если вы выберете опцию добавить промокод,\nу вас будет шанс включить уникальный промокод, который вы сможете продвигать у себя.\n\nБез промокода 🚫:\n ♦️ Если вы решите не использовать промокод, вы получите набор картинок, но без специальных предложений.\n\nДобавить промокод в баннер?🏷️",
            'enter_promo_text': "✍️ Введите, пожалуйста,  текст промокода:",
            'promo_no_exists': "❌ Данная акция больше не существует ❌",
            'zip_without_promo': "Вот твой zip-архив!\nСоздал без промокода, как Вы и просили 😉",
            'zip_with_promo': "Смотри, твой zip-архив с промокодом готов!\n🎉🔥 Красота, правда?",
            'enter_correct_promo': "Пожалуйста, введи корректный промокод. 😜 Не теряйте шанс!",
            'faq': "❓ <b>Вопросы и ответы (FAQ)</b>"
        },
        'en': {
            'change_key': "Welcome to the support section! 📚\nHere you can check out the FAQ section, where the most popular answers to users' questions are gathered.\nWe have prepared useful tips and recommendations for you so that you can quickly find the information you need and easily resolve any issues that may arise.\n\nChange Language! 🌐\nYou can also easily change the bot's language. Just select your preferred language, and all messages will be displayed in it.",
            'select_language': "🌍 Choose a language for uploading banners, and they will be displayed in the language you selected.",
            'select_banners': "Choose the type of banners! 🎰\n\nBasic banners 🏷️:\n ❗️ Here are all the basic offers!\n\nPromo 🎁:\n ❗️ In this section, you can also choose other relevant offers and promotions, participation in which will give bonuses or free bets.\n\nNext, if you choose the option with promo codes, you'll receive banners that activate additional discounts.\nIf you choose without a promo code, you'll get an archive with relevant offers, without a promo code.",
            'add_promo': "With a promo code ✨:\n ♦️ If you choose the option to add a promo code,\nyou will have a chance to activate a unique promo code that you can promote.\n\nWithout a promo code 🚫:\n ♦️ If you decide not to use a promo code, you will receive a set of images, but without special offers.\n\nAdd a promo code to the banner?🏷️",
            'enter_promo_text': "✍️ Please enter the promo code text:",
            'promo_no_exists': "❌ This promotion no longer exists ❌",
            'zip_without_promo': "Here’s your zip archive! Created without a promo code, as you requested 😉",
            'zip_with_promo': "Look, your zip archive with a promo code is ready!\n🎉🔥 Isn’t it beautiful?",
            'enter_correct_promo': "Please enter a valid promo code. 😜 Don't miss your chance!",
            'faq': "❓ <b>Questions and Answers (FAQ)</b>"
        },
        'uz': {
            'change_key': "Qo'llab-quvvatlash bo'limiga xush kelibsiz! 📚\nBu yerda siz foydalanuvchilar savollariga eng mashhur javoblar to'plangan FAQ bo'limi bilan tanishishingiz mumkin.\nSizga kerakli ma'lumotni tezda topish va yuzaga keladigan har qanday muammolarni osonlik bilan hal qilish uchun foydali maslahatlar va tavsiyalar tayyorladik.\n\nTilni o'zgartiring! 🌐\nShuningdek, botning tilini osonlik bilan o'zgartirishingiz mumkin. Faqatgina afzal ko'rgan tilni tanlang va barcha xabarlar shu tilda ko'rsatiladi.",
            'select_language': "🌍 Bannerlarni yuklash uchun tilni tanlang, va ular siz tanlagan tilda ko'rsatiladi.",
            'select_banners': "Banner turlarini tanlang! 🎰\n\nBasic bannerlar 🏷️:\n ❗️ Bu yerda barcha asosiy takliflar to'plangan!\n\nPromo 🎁:\n ❗️ Ushbu bo'limda siz boshqa dolzarb takliflar va aksiyalardan ham tanlashingiz mumkin, ularda ishtirok etish bonuslar yoki fribetlar beradi.\n\nKeyinchalik, agar siz promokodlar bilan variantni tanlasangiz, qo'shimcha chegirmalarni faollashtiruvchi bannerlar olasiz.\nAgar promokodsiz variantni tanlasangiz, sizni promokodsiz dolzarb takliflar arxivi kutmoqda.",
            'add_promo': "Promokod bilan ✨:\n ♦️ Agar siz promokodni qo'shish variantini tanlasangiz,\n sizga o'zingiz reklama qilishingiz mumkin bo'lgan noyob promokodni faollashtirish imkoniyati beriladi.\n\nPromokodsiz 🚫:\n ♦️ Agar siz promokodni ishlatmaslikka qaror qilsangiz, sizga rasm to'plami beriladi, ammo maxsus takliflarsiz.\n\nBannerga promokod qo'shasizmi?🏷️",
            'enter_promo_text': "✍️ Iltimos, promokod matnini kiriting:",
            'promo_no_exists': "❌ Ushbu aksiya endi mavjud emas ❌",
            'zip_without_promo': "Mana sizning zip arxivingiz!\nSiz so'raganingizdek, promokodsiz yaratildi 😉",
            'zip_with_promo': "Qarang, sizning promokodli zip arxivingiz tayyor!\n🎉🔥 Chiroyli emasmi?",
            'enter_correct_promo': "Iltimos, to'g'ri promokodni kiriting.\n😜 O'z imkoniyatingizni boy bermang!",
            'faq': "❓ <b>Savollar va javoblar (FAQ)</b>"
        }
    }
    # Получаем фразу по ключу и языку
    return phrases.get(language, {}).get(key, "Фраза не найдена")