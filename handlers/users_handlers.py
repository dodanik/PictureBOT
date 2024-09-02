import os
import re
import shutil
import zipfile

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from drawing_function.drawing_function import process_images_and_add_text
from dynamic_and_static_data.dynamic_and_static_data import get_botlang, save_botlang, get_banners
from filters.chat_type_filter import ChatTypesFilter
from aiogram import types, F

from func.filter_promoactions_user import get_keys_with_visibility
from keyboards.user.create_kb_promoactions import create_kb_promoactions
from keyboards.user.data_text_message import get_text_message
from keyboards.user.general_menu_kb import create_general_menu
from keyboards.user.kb_bot_lang import get_language_keyboard
from keyboards.user.kb_download_select_lang import create_download_lang_menu
from keyboards.user.promo_basic_confirm_kb import create_promo_code_basic_confirm_kb
from keyboards.user.promocode_confirmation import create_promo_code_confirm_kb
from keyboards.user.settings_user_menu import create_settings_menu

user_router = Router()
user_router.message.filter(ChatTypesFilter(['private']))






class Download(StatesGroup):
    lang = State()
    name_baner = State()
    promocode = State()


class DownloadBBanners(StatesGroup):
    lang = State()
    name_baner = State()
    promocode = State()





@user_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("You have entered the Name banner bot, please select a language",
                         reply_markup=await get_language_keyboard())


@user_router.callback_query(lambda c: c.data.startswith('lang_'))
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    # Извлекаем данные из callback_data
    language_code = callback_query.data
    botlang = await get_botlang()

    # Определяем ответ в зависимости от языка
    if language_code == 'lang_ru':
        botlang[callback_query.message.chat.id] = 'ru'
        response_text = "Вы выбрали русский язык."
    elif language_code == 'lang_en':
        botlang[callback_query.message.chat.id] = 'en'
        response_text = "You selected English."
    elif language_code == 'lang_uz':
        botlang[callback_query.message.chat.id] = 'uz'
        response_text = "Siz o'zbek tilini tanladingiz."
    else:
        response_text = "Язык не выбран."

    # Отправляем ответ пользователю
    await callback_query.message.answer(response_text, reply_markup=await create_general_menu(botlang[callback_query.message.chat.id]))

    # Удаляем инлайн-клавиатуру, если необходимо
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await save_botlang(botlang)







@user_router.message((F.text == "Settings") | (F.text == "Настройки") | (F.text == "Sozlamalar"))
async def settings(message: types.Message, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    await message.answer(f"{await get_text_message(botlang[message.chat.id], 'change_key')}",
                         reply_markup=await create_settings_menu(botlang[message.chat.id]))


@user_router.callback_query(lambda c: c.data.startswith('setting_lang'))
async def settings_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_reply_markup(reply_markup=await get_language_keyboard())




@user_router.message((F.text == "Download") | (F.text == "Скачать") | (F.text == "Yuklab olish"))
async def download(message: types.Message, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    await message.answer(f"{await get_text_message(botlang[message.chat.id], 'select_language')}",
                         reply_markup=await create_download_lang_menu())



@user_router.callback_query(lambda c: c.data.startswith('dw_lang_'))
async def download_lang_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    banners = await get_banners()
    lang_selected = callback_query.data.split('_')[-1] or "en"
    names_array = await get_keys_with_visibility(banners, lang_selected)
    await callback_query.message.answer(f"{await get_text_message(botlang[callback_query.message.chat.id], 'select_banners')}",
                                        reply_markup=await create_kb_promoactions(names_array, lang_selected))





@user_router.callback_query(lambda c: c.data.startswith('NM_BN_'))
async def download_name_baner_promo_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    text = callback_query.data.split("NM_BN_", 1)[1]
    name_offer, lang = text.rsplit('_', 1)
    await callback_query.message.answer(f"{await get_text_message(botlang[callback_query.message.chat.id], 'add_promo')}", reply_markup=await create_promo_code_confirm_kb(name_offer, lang, botlang[callback_query.message.chat.id]))


@user_router.callback_query(lambda c: c.data.startswith('dwnl_'))
async def download_confirm_promo_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    banners = await get_banners()

    if "dwnl_promo_" in callback_query.data:
        text = callback_query.data.split("dwnl_promo_", 1)[1]
        name_offer_text, lang = text.rsplit('_', 1)
        name_offer = name_offer_text.replace('_', ' ')
        if name_offer in banners:
            await callback_query.message.answer(f"{await get_text_message(botlang[callback_query.message.chat.id], 'enter_promo_text')}")
            await state.set_state(Download.promocode)
            await state.update_data(lang=lang, name_baner=name_offer)
        else:
            await callback_query.message.answer(f"{await get_text_message(botlang[callback_query.message.chat.id], 'promo_no_exists')}")
    elif "dwnl_no_" in callback_query.data:
        text = callback_query.data.split("dwnl_no_", 1)[1]
        name_offer_text, lang = text.rsplit('_', 1)
        name_offer = name_offer_text.replace('_', ' ')
        if banners[name_offer].get("visibility"):
            no_promo_paths = banners[name_offer].get(lang, {}).get("no_promo", [])
            temp_dir = os.path.join(".", f"temp_{callback_query.message.chat.id}")
            os.makedirs(temp_dir, exist_ok=True)
            new_paths = []
            # Копируем файлы и сохраняем новые пути
            for path in no_promo_paths:
                # Получаем имя файла из пути
                filename = os.path.basename(path)
                # Формируем новый путь в директории temp_dir
                new_path = os.path.join(temp_dir, filename)
                # Копируем файл
                shutil.copy(path, new_path)
                # Добавляем новый путь в список
                new_paths.append(new_path)
            zip_filename = os.path.join(temp_dir, f"{name_offer}.zip")

            # Создаем ZIP-архив
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                # Проходим по всем файлам в директории temp_dir
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Добавляем файл в архив, исключая сам архив, если он уже существует
                        if file_path != zip_filename:
                            zipf.write(file_path, os.path.relpath(file_path, temp_dir))

            await callback_query.message.answer_document(document=FSInputFile(zip_filename),
                                         caption=f"{await get_text_message(botlang[callback_query.message.chat.id], 'zip_without_promo')}")
            shutil.rmtree(temp_dir)
            await state.clear()

@user_router.message(Download.promocode, F.text)
async def download_promocode(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    banners = await get_banners()
    data = await state.get_data()
    position_promo = banners[data['name_baner']].get("position_promo")
    if message.text:
        if re.match(r'^[A-Za-z0-9]{1,20}$', message.text):
            if banners[data['name_baner']].get("visibility"):
                promo_paths = banners[data['name_baner']].get(data['lang'], {}).get("promo", [])
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)
                new_paths = []
                # Копируем файлы и сохраняем новые пути
                for path in promo_paths:
                    # Получаем имя файла из пути
                    filename = os.path.basename(path)
                    # Формируем новый путь в директории temp_dir
                    new_path = os.path.join(temp_dir, filename)
                    # Копируем файл
                    shutil.copy(path, new_path)
                    # Добавляем новый путь в список
                    new_paths.append(new_path)
                await process_images_and_add_text(new_paths, message.text, position_promo)
                zip_filename = os.path.join(temp_dir, f"{data['name_baner']}.zip")

                # Создаем ZIP-архив
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    # Проходим по всем файлам в директории temp_dir
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Добавляем файл в архив, исключая сам архив, если он уже существует
                            if file_path != zip_filename:
                                zipf.write(file_path, os.path.relpath(file_path, temp_dir))


                await message.reply_document(document=FSInputFile(zip_filename), caption=f"{await get_text_message(botlang[message.chat.id], 'zip_with_promo')}")
                shutil.rmtree(temp_dir)
            await state.clear()
        else:
            await message.answer(f"{await get_text_message(botlang[message.chat.id], 'enter_correct_promo')}")
            await state.set_state(Download.promocode)



@user_router.callback_query(lambda c: c.data.startswith('basic_bnrs_'))
async def download_name_baner_basic_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    text = callback_query.data.split("basic_bnrs_", 1)[1]
    await callback_query.message.answer(f"{await get_text_message(botlang[callback_query.message.chat.id], 'add_promo')}", reply_markup=await create_promo_code_basic_confirm_kb(text, botlang[callback_query.message.chat.id]))


@user_router.callback_query(lambda c: c.data.startswith('basic_dwnl_'))
async def download_confirm_promo_basic_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    banners = await get_banners()

    if "basic_dwnl_pr_" in callback_query.data:
        lang = callback_query.data.split("basic_dwnl_pr_", 1)[1]
        await callback_query.message.answer(
            f"{await get_text_message(botlang[callback_query.message.chat.id], 'enter_promo_text')}")
        await state.set_state(DownloadBBanners.promocode)
        await state.update_data(lang=lang)

    elif "basic_dwnl_no_" in callback_query.data:
        lang = callback_query.data.split("basic_dwnl_no_", 1)[1]
        basic_banners = banners.get('basic_banners', {})
        no_promo_paths = []

        # Проходим по всем баннерам в basic_banners
        for banner_name, banner_info in basic_banners.items():
            if banner_info.get('visibility', False):  # Проверяем, видим ли баннер
                # Получаем пути к файлам для указанного языка
                lang_paths = banner_info.get(lang, {})
                no_promo_paths.extend(lang_paths.get('no_promo', []))
                temp_dir = os.path.join(".", f"temp_{callback_query.message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)
                new_paths = []
                # Копируем файлы и сохраняем новые пути
                for path in no_promo_paths:
                    # Получаем имя файла из пути
                    filename = os.path.basename(path)
                    # Формируем новый путь в директории temp_dir
                    new_path = os.path.join(temp_dir, filename)
                    # Копируем файл
                    shutil.copy(path, new_path)
                    # Добавляем новый путь в список
                    new_paths.append(new_path)
                zip_filename = os.path.join(temp_dir, "Basic Banners.zip")

                # Создаем ZIP-архив
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    # Проходим по всем файлам в директории temp_dir
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Добавляем файл в архив, исключая сам архив, если он уже существует
                            if file_path != zip_filename:
                                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

                await callback_query.message.answer_document(document=FSInputFile(zip_filename),
                                             caption=f"{await get_text_message(botlang[callback_query.message.chat.id], 'zip_without_promo')}")
                shutil.rmtree(temp_dir)
                await state.clear()

@user_router.message(DownloadBBanners.promocode, F.text)
async def download_promocode_basic(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    banners = await get_banners()
    data = await state.get_data()
    if message.text:
        if re.match(r'^[A-Za-z0-9]{1,20}$', message.text):
            basic_banners = banners.get('basic_banners', {})

            promo_paths = []

            # Проходим по всем баннерам в basic_banners
            for banner_name, banner_info in basic_banners.items():
                if banner_info.get('visibility', False):  # Проверяем, видим ли баннер
                    # Получаем пути к файлам для указанного языка
                    lang_paths = banner_info.get(data["lang"], {})
                    promo_paths.extend(lang_paths.get('promo', []))
                    temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                    os.makedirs(temp_dir, exist_ok=True)
                    new_paths = []
                    # Копируем файлы и сохраняем новые пути
                    for path in promo_paths:
                        # Получаем имя файла из пути
                        filename = os.path.basename(path)
                        # Формируем новый путь в директории temp_dir
                        new_path = os.path.join(temp_dir, filename)
                        # Копируем файл
                        shutil.copy(path, new_path)
                        # Добавляем новый путь в список
                        new_paths.append(new_path)
                    await process_images_and_add_text(new_paths, message.text)
                    zip_filename = os.path.join(temp_dir, "Basic Banners.zip")

                    # Создаем ZIP-архив
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        # Проходим по всем файлам в директории temp_dir
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Добавляем файл в архив, исключая сам архив, если он уже существует
                                if file_path != zip_filename:
                                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))


                    await message.reply_document(document=FSInputFile(zip_filename), caption=f"{await get_text_message(botlang[message.chat.id], 'zip_with_promo')}")
                    shutil.rmtree(temp_dir)
                await state.clear()
        else:
            await message.answer(f"{await get_text_message(botlang[message.chat.id], 'enter_correct_promo')}")
            await state.set_state(DownloadBBanners.promocode)
