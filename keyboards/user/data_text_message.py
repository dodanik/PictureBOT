async def get_text_message(language, key):
    # Словарь с переводами фраз
    phrases = {
        'ru': {
            'change_key': "<b>Добро пожаловать в раздел поддержки!</b> 👋\nВы можете задать свой вопрос прямо сейчас, и наш специалист с радостью ответит на ваш запрос!\n \nХотите сменить язык? 🌐\nЭто легко! Просто выберите свой язык, и все сообщения будут отображаться на нем.",
            'select_language': "🌍 Выберите язык для загрузки баннеров, и они будут отображаться именно на выбранном вами языке.",
            'select_banners': "<b>Выберите тип баннеров!</b> 🎰\n\n<b>Basic banners 🏷️:</b>\n ❗️ Здесь собраны все основные предложения!\n\n<b>Promo</b> 🎁:\n ❗️ В данном разделе Вы так же можете выбрать и другие актуальные предложения и акции, участие в которых будет давать бонусы или фрибеты.\n\nДалее, если вы выберете опцию с промокодами, получите баннеры, которые активируют дополнительные скидки.\nЕсли же выберете без промокода, вас ждет архив с актуальными предложениями, без промокода.",
            'add_promo': "<b>С промокодом ✨:</b>\n ♦️ Если вы выберете опцию добавить промокод,\nу вас будет шанс включить уникальный промокод, который вы сможете продвигать у себя.\n\n<b>Без промокода 🚫:</b>\n ♦️ Если вы решите не использовать промокод, вы получите набор картинок, но без специальных предложений.\n\nДобавить промокод в баннер?🏷️",
            'enter_promo_text': "✍️ Введите, пожалуйста,  текст промокода:",
            'promo_no_exists': "❌ Данная акция больше не существует ❌",
            'zip_without_promo': "Вот твой zip-архив!\nСоздал без промокода, как Вы и просили 😉",
            'zip_with_promo': "Смотри, твой zip-архив с промокодом готов!\n🎉🔥 Красота, правда?",
            'enter_correct_promo': "Пожалуйста, введи корректный промокод. 😜 Не теряйте шанс!",
            'faq': "❓ <b>Вопросы и ответы (FAQ)</b>"
        },
        'en': {
            'change_key': "<b>Welcome to the support section!</b> 👋\nYou can ask your question right now, and our specialist will be happy to respond to your request!\n\nWant to change the language? 🌐\nIt's easy! Just select your language, and all messages will be displayed in it.",
            'select_language': "🌍 Choose a language for uploading banners, and they will be displayed in the language you selected.",
            'select_banners': "<b>Choose the type of banners!</b> 🎰\n\n<b>Basic banners 🏷️:</b>\n ❗️ Here are all the basic offers!\n\n<b>Promo</b> 🎁:\n ❗️ In this section, you can also choose other relevant offers and promotions, participation in which will give bonuses or free bets.\n\nNext, if you choose the option with promo codes, you'll receive banners that activate additional discounts.\nIf you choose without a promo code, you'll get an archive with relevant offers, without a promo code.",
            'add_promo': "<b>With a promo code ✨:</b>\n ♦️ If you choose the option to add a promo code,\nyou will have a chance to activate a unique promo code that you can promote.\n\n<b>Without a promo code 🚫:</b>\n ♦️ If you decide not to use a promo code, you will receive a set of images, but without special offers.\n\nAdd a promo code to the banner?🏷️",
            'enter_promo_text': "✍️ Please enter the promo code text:",
            'promo_no_exists': "❌ This promotion no longer exists ❌",
            'zip_without_promo': "Here’s your zip archive! Created without a promo code, as you requested 😉",
            'zip_with_promo': "Look, your zip archive with a promo code is ready!\n🎉🔥 Isn’t it beautiful?",
            'enter_correct_promo': "Please enter a valid promo code. 😜 Don't miss your chance!",
            'faq': "❓ <b>Questions and Answers (FAQ)</b>"
        },
        'uz': {
            'change_key': "<b>Qo'llab-quvvatlash bo'limiga xush kelibsiz!</b> 👋\nSiz hozirda savolingizni berishingiz mumkin, va bizning mutaxassisimiz sizning so'rovingizga mamnuniyat bilan javob beradi!\n\nTilni o'zgartirmoqchimisiz? 🌐\nBu oson! Faqat o'zingizga qulay tilni tanlang, va barcha xabarlar shunda ko'rsatiladi.",
            'select_language': "🌍 Bannerlarni yuklash uchun tilni tanlang, va ular siz tanlagan tilda ko'rsatiladi.",
            'select_banners': "<b>Banner turlarini tanlang!</b> 🎰\n\n<b>Basic bannerlar 🏷️:</b>\n ❗️ Bu yerda barcha asosiy takliflar to'plangan!\n\n<b>Promo 🎁:</b>\n ❗️ Ushbu bo'limda siz boshqa dolzarb takliflar va aksiyalardan ham tanlashingiz mumkin, ularda ishtirok etish bonuslar yoki fribetlar beradi.\n\nKeyinchalik, agar siz promokodlar bilan variantni tanlasangiz, qo'shimcha chegirmalarni faollashtiruvchi bannerlar olasiz.\nAgar promokodsiz variantni tanlasangiz, sizni promokodsiz dolzarb takliflar arxivi kutmoqda.",
            'add_promo': "<b>Promokod bilan ✨:</b>\n ♦️ Agar siz promokodni qo'shish variantini tanlasangiz,\n sizga o'zingiz reklama qilishingiz mumkin bo'lgan noyob promokodni faollashtirish imkoniyati beriladi.\n\n<b>Promokodsiz 🚫:</b>\n ♦️ Agar siz promokodni ishlatmaslikka qaror qilsangiz, sizga rasm to'plami beriladi, ammo maxsus takliflarsiz.\n\nBannerga promokod qo'shasizmi?🏷️",
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