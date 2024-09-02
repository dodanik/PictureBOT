import asyncio
import os
import re
import zipfile
import shutil

from aiogram import Router
from aiogram import Bot, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from drawing_function.drawing_function import process_images_and_add_text
from dynamic_and_static_data.dynamic_and_static_data import get_botlang, save_botlang, get_banners, save_banners
from filters.chat_type_filter import ChatTypesFilter, IsAdmin, get_my_admins_list, my_admins_list_add, \
    my_admins_list_remove
from func.update_banners_list import update_banners_list
from keyboards.admin.addStock.admin_add_stock_menu import admin_add_stock_menu
from keyboards.admin.addStock.confirmation_banners import confirmation_banners_kb
from keyboards.admin.delete.delete_menu import create_delete_menu_kb
from keyboards.admin.delete.dell_list_offer_kb import create_del_list_offer_kb
from keyboards.admin.delete.remove_apply_kb import create_remove_apply_kb
from keyboards.admin.general_menu_admin_kb import general_menu_admins_kb
from keyboards.admin.inline_admin_kb import kb_upload
from keyboards.admin.addStock.promocode_lication_kb import location_promocode_kb
from keyboards.admin.change.cahnge_location_promocode import create_change_location_promocode_kb
from keyboards.admin.change.change_data_promo import create_change_data_promo_kb
from keyboards.admin.change.change_data_zip_offer_kb import create_change_data_zip_offer_kb
from keyboards.admin.change.change_menu_start import create_kb_chang
from keyboards.admin.change.change_name_offer_kb import create_change_name_offer_kb
from keyboards.admin.change.change_visibility import create_change_visibility_kb
from keyboards.admin.change.menu_list_change_banners import create_list_change_banners_kb
from keyboards.admin.change.toggle_visibility_kb import create_toggle_visibility_kb
from keyboards.admin.settings_kb import create_kb_change_admin

admin_router = Router()
admin_router.message.filter(ChatTypesFilter(['private']), IsAdmin())






class AddStockBasicBanners(StatesGroup):
    stock_name = State()
    data_zip = State()
    file_info = State()


class AddStockPromo(StatesGroup):
    stock_name = State()
    promocode_location = State()
    data_zip = State()
    file_info = State()


class AddAdmin(StatesGroup):
    user_id = State()
    user_name = State()

class DeleteAdmin(StatesGroup):
    user_id = State()
    user_name = State()


@admin_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Hello Admin!", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
    botlang = await get_botlang()
    botlang[message.chat.id] = 'en'
    await save_botlang(botlang)





@admin_router.message(F.text == "Settings")
async def settings_menu_admin(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Admin management:", reply_markup=await create_kb_change_admin())


@admin_router.callback_query(lambda c: c.data.startswith('select_admin_'))
async def add_del_admin_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if callback_query.data == "select_admin_add_admin":
        await callback_query.message.answer("Enter the telegram ID of the new admin (Numbers only)", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddAdmin.user_id)
    elif callback_query.data == "select_admin_del_admin":
        admins = await get_my_admins_list()
        await callback_query.message.answer("Admins now:", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        for admin in admins:
            await callback_query.message.answer(f"{admin}")
        await callback_query.message.answer("Enter the ID of the admin you want to delete", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(DeleteAdmin.user_id)



@admin_router.message(AddAdmin.user_id,(F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def add_admin(message: types.Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        await my_admins_list_add(admin_id)
        await state.clear()
        await message.answer("Admin ADDED!", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
    except ValueError:
        await message.answer("You entered an incorrect user ID.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.clear()


@admin_router.message(DeleteAdmin.user_id, (F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def del_admin(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id != int(message.text):
            if int(message.text) not in [5233415694, 270770023]:
                remove_admin_list = await my_admins_list_remove(int(message.text))
                admin_list = await get_my_admins_list()
                if remove_admin_list:
                    await message.answer(f"Admin REMOVED!\n List of admins:")
                    for admin in admin_list:
                        await message.answer(f"{admin}", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                else:
                    await message.answer(f"Administrator with this ID was not found\n List of admins:\n {admin_list}", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))

            else:
                await message.answer("Just try to take aim at the main one!", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))

        else:
            await message.answer("YOU CAN'T DELETE YOURSELF)))", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.clear()
    except ValueError:
        await message.answer("You entered an incorrect user ID.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.clear()



@admin_router.message(F.text == "Upload")
async def uploadData(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Select what needs to be done:", reply_markup=kb_upload.as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data.startswith('action_'))
async def upload_process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    # Извлекаем данные из callback_data
    action = callback_query.data

    if action == 'action_add':
        # await callback_query.message.edit_reply_markup(reply_markup=None)
        # Отправляем ответ пользователю
        await callback_query.message.answer("Select what to add:",
                                            reply_markup=await admin_add_stock_menu())
    elif action == 'action_change':

        await callback_query.message.answer("Select what to change:",
                                            reply_markup=await create_kb_chang())

    elif action == 'action_delete':
        await callback_query.message.answer("Select what to delete:", reply_markup=await create_delete_menu_kb())


@admin_router.callback_query(lambda c: c.data.startswith('add_stock_'))
async def upload_add_stock_process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    action = callback_query.data
    if action == "add_stock_basic_baner":
        await callback_query.message.answer("Please send the offer name (Basic banners):",
                                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.stock_name)
    elif action == "add_stock_promo":
        await callback_query.message.answer("Please send the offer name (Promo):",
                                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockPromo.stock_name)





#_____________________________________________AddStockBasicBanners

@admin_router.message(AddStockBasicBanners.stock_name, (F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def add_name_stock_basic_banner(message: types.Message, state: FSMContext):
    if message.text:
        words = message.text.split()
        if all(re.fullmatch(r'^[A-Za-z0-9!@#$%&*()€]{1,42}$', word) for word in words):
            await state.update_data(stock_name=message.text)
            await message.answer("Send a zip archive with images",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(AddStockBasicBanners.data_zip)
        else:
            await message.answer("Please enter the correct banner name(Maximum 42 characters)",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(AddStockBasicBanners.stock_name)
    else:
        await message.answer("Please enter the correct banner name:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.stock_name)









@admin_router.message(AddStockBasicBanners.data_zip, F.document)
async def handle_basic_banner_zip_file(message: types.Message, bot: Bot, state: FSMContext):
    # Проверка, что файл является ZIP архивом
    if not message.document.file_name.endswith('.zip'):
        await message.reply("Please send a ZIP archive.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.data_zip)
    else:
        LANGUAGES = ['az', 'uz', 'kz', 'tr', 'ru', 'en', 'br', 'ng']
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']

        # Загрузка архива
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(file_info=file_info.file_path)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Проверка наличия файлов нужного типа в архиве
        with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(file.lower().endswith(tuple(ALLOWED_EXTENSIONS)) for file in file_list):
                await message.reply(
                    "The archive does not contain supported files (JPEG). Please send an archive with JPEG images.",
                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.set_state(AddStockBasicBanners.data_zip)
            else:
                # Создание уникальной временной директории для распаковки
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)

                # Распаковка ZIP-архива
                zip_ref.extractall(temp_dir)

            # Группировка файлов по языковым окончаниям
            language_groups = {}
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    for lang in LANGUAGES:
                        if file.endswith(f'_{lang}.jpg') or file.endswith(f'_{lang}.jpeg'):  # Поддерживаемые форматы
                            relative_path = os.path.relpath(os.path.join(root, file), ".")
                            if lang not in language_groups:
                                language_groups[lang] = []
                            language_groups[lang].append(relative_path)

            # Отправка файлов по группам
            for lang, files in language_groups.items():
                if files:
                    # Создание медиагруппы
                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()
                    promo_files = [file for file in files if '_promo_' in file]
                    if promo_files:
                        await process_images_and_add_text(promo_files, "TEST")

                    for file_path in files:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1/3)

            await message.answer("Add banners?", reply_markup=await confirmation_banners_kb())

            # Удаление временной директории и её содержимого
            shutil.rmtree(temp_dir)
            await state.set_state(AddStockBasicBanners.file_info)


@admin_router.callback_query(AddStockBasicBanners.file_info, lambda c: c.data.startswith('confirmation_banners_'))
async def upload_confirmation_banners_process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    action = callback_query.data
    banners = await get_banners()
    if action == 'confirmation_banners_remake':
        await callback_query.message.answer("Select what to add:",
                                            reply_markup=await admin_add_stock_menu())
        await state.clear()

    elif action == 'confirmation_banners_apply':
        data = await state.get_data()
        downloaded_file = await bot.download_file(data['file_info'])
        os.makedirs(os.path.join('stock_data', 'basic_banners', data['stock_name']), exist_ok=True)

        main_folder_path = os.path.join("stock_data", "basic_banners", data['stock_name'])

        with zipfile.ZipFile(downloaded_file) as archive:
            for file_name in archive.namelist():
                if '_' in file_name:
                    # Определение типа промо
                    if '_promo_' in file_name:
                        promo_type = 'promo'
                    else:
                        promo_type = 'no_promo'

                    # Извлечение языка (после последнего '_')
                    suffix = file_name.split('_')[-1].split('.')[0]
                    language = suffix  # Язык находится в конце имени файла перед расширением

                    # Определение пути к папке для извлечения
                    folder_path = os.path.join(main_folder_path, language, promo_type)

                    # Создание папки для языка и типа промо
                    os.makedirs(folder_path, exist_ok=True)

                    # Определение имени файла без путей
                    file_name_without_path = os.path.basename(file_name)

                    # Полный путь для извлечения
                    extract_path = os.path.join(folder_path, file_name_without_path)

                    # Извлечение файла
                    with open(extract_path, 'wb') as out_file:
                        out_file.write(archive.read(file_name))
                    if data['stock_name'] not in banners['basic_banners']:
                        banners['basic_banners'][data['stock_name']] = {'visibility': True}

                    # Заполнение словаря баннеров
                    if language not in banners['basic_banners'][data['stock_name']]:
                        banners['basic_banners'][data['stock_name']][language] = {'promo': [], 'no_promo': []}

                    # Добавление пути к файлу в соответствующий массив
                    relative_path = os.path.relpath(extract_path, ".")
                    banners['basic_banners'][data['stock_name']][language][promo_type].append(relative_path)
        await state.clear()
        await save_banners(banners)
        await callback_query.message.reply(f"Promotion {data['stock_name']} added successfully to Basic banners!",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))







#_____________________________________________AddStockPromo
@admin_router.message(AddStockPromo.stock_name, (F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def add_name_stock_promo_banner(message: types.Message, state: FSMContext, bot: Bot):
    files = ["img/bottom_left.png", "img/top_bottom.png", "img/top_cener.png"]
    if message.text:
        words = message.text.split()
        if all(re.fullmatch(r'^[A-Za-z0-9!@#$%&*()€]{1,42}$', word) for word in words):
            await state.update_data(stock_name=message.text)
            await message.answer("Example of location:", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True) )
            for file_path in files:
                await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(file_path))

            await message.answer("Select the location of the promo code:",
                                 reply_markup=await location_promocode_kb())
            await state.set_state(AddStockPromo.promocode_location)
        else:
            await message.answer("Please enter the correct banner name(Maximum 42 characters):",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(AddStockPromo.stock_name)
    else:
        await message.answer("Please enter the correct banner name:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockPromo.stock_name)


# Обработчик нажатий на кнопки выбора
@admin_router.callback_query(AddStockPromo.promocode_location, lambda c: c.data and c.data.startswith('location_promocode_'))
async def process_location_promo_promocode(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data

    if "location_promocode_apply_" in data:
        selected_text = data.split("location_promocode_apply_")[1]
        await state.update_data(promocode_location=selected_text.lower())
        await callback_query.message.answer("Send a zip archive with images",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockPromo.data_zip)
    else:
        # Обновление выбора
        selected = data.replace("location_promocode_", "").replace("_", " ")
        # Обновляем клавиатуру с выбранной кнопкой
        keyboard = await location_promocode_kb(selected)
        await callback_query.message.edit_text("Please select an option:", reply_markup=keyboard)



@admin_router.message(AddStockPromo.data_zip, F.document)
async def handle_promo_banner_zip_file(message: types.Message, bot: Bot, state: FSMContext):
    # Проверка, что файл является ZIP архивом
    if not message.document.file_name.endswith('.zip'):
        await message.reply("Please send a ZIP archive.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockPromo.data_zip)
    else:
        LANGUAGES = ['az', 'uz', 'kz', 'tr', 'ru', 'en', 'br', 'ng']
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']

        # Загрузка архива
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(file_info=file_info.file_path)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Проверка наличия файлов нужного типа в архиве
        with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(file.lower().endswith(tuple(ALLOWED_EXTENSIONS)) for file in file_list):
                await message.reply(
                    "The archive does not contain supported files (JPEG). Please send an archive with JPEG images.",
                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.set_state(AddStockPromo.data_zip)
            else:
                # Создание уникальной временной директории для распаковки
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)

                # Распаковка ZIP-архива
                zip_ref.extractall(temp_dir)

            # Группировка файлов по языковым окончаниям
            language_groups = {}
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    for lang in LANGUAGES:
                        if file.endswith(f'_{lang}.jpg') or file.endswith(f'_{lang}.jpeg'):  # Поддерживаемые форматы
                            relative_path = os.path.relpath(os.path.join(root, file), ".")
                            if lang not in language_groups:
                                language_groups[lang] = []
                            language_groups[lang].append(relative_path)

            # Отправка файлов по группам
            for lang, files in language_groups.items():
                if files:
                    # Создание медиагруппы
                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()
                    promocode_location = data_state["data_state"]
                    promo_files = [file for file in files if '_promo_' in file]
                    if promo_files:
                        await process_images_and_add_text(promo_files, "TEST", promocode_location)

                    for file_path in files:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1/3)

            await message.answer("Add banners?", reply_markup=await confirmation_banners_kb())

            # Удаление временной директории и её содержимого
            shutil.rmtree(temp_dir)
            await state.set_state(AddStockPromo.file_info)


@admin_router.callback_query(AddStockPromo.file_info, lambda c: c.data.startswith('confirmation_banners_'))
async def upload_confirmation_promo_banners_process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    action = callback_query.data
    banners = await get_banners()
    if action == 'confirmation_banners_remake':
        await callback_query.message.answer("Select what to add:",
                                            reply_markup=await admin_add_stock_menu())
        await state.clear()

    elif action == 'confirmation_banners_apply':
        data = await state.get_data()
        downloaded_file = await bot.download_file(data['file_info'])
        os.makedirs(os.path.join('stock_data', data['stock_name']), exist_ok=True)

        main_folder_path = os.path.join("stock_data", data['stock_name'])

        with zipfile.ZipFile(downloaded_file) as archive:
            for file_name in archive.namelist():
                if '_' in file_name:
                    # Определение типа промо
                    if '_promo_' in file_name:
                        promo_type = 'promo'
                    else:
                        promo_type = 'no_promo'

                    # Извлечение языка (после последнего '_')
                    suffix = file_name.split('_')[-1].split('.')[0]
                    language = suffix  # Язык находится в конце имени файла перед расширением

                    # Определение пути к папке для извлечения
                    folder_path = os.path.join(main_folder_path, language, promo_type)

                    # Создание папки для языка и типа промо
                    os.makedirs(folder_path, exist_ok=True)

                    # Определение имени файла без путей
                    file_name_without_path = os.path.basename(file_name)

                    # Полный путь для извлечения
                    extract_path = os.path.join(folder_path, file_name_without_path)

                    # Извлечение файла
                    with open(extract_path, 'wb') as out_file:
                        out_file.write(archive.read(file_name))
                    if data['stock_name'] not in banners:
                        banners[data['stock_name']] = {'visibility': True, 'position_promo': data['promocode_location']}

                    # Заполнение словаря баннеров
                    if language not in banners[data['stock_name']]:
                        banners[data['stock_name']][language] = {'promo': [], 'no_promo': []}

                    # Добавление пути к файлу в соответствующий массив
                    relative_path = os.path.relpath(extract_path, ".")
                    banners[data['stock_name']][language][promo_type].append(relative_path)
        await state.clear()
        await save_banners(banners)
        await callback_query.message.reply(f"Promotion {data['stock_name']} added successfully to Promo!",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))










#_____________________________________________Change




@admin_router.callback_query(lambda c: c.data.startswith('change_start_'))
async def change_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    data = callback_query.data

    if data == "change_start_basic_banners":
        button_click = data.split("change_start_")[1]
        await callback_query.message.answer("Choose what you want to change(Basic banners)?", reply_markup=await create_change_visibility_kb(button_click))

    if data == "change_start_promo":
        button_click = data.split("change_start_")[1]
        await callback_query.message.answer("Choose what you want to change(Promo)?",
                                            reply_markup=await create_change_visibility_kb(button_click))



@admin_router.callback_query(lambda c: c.data.startswith('change_selecting_section_'))
async def change_menu_selecting_section(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    banners = await get_banners()
    data = callback_query.data

    if data == "change_selecting_section_basic_banners_visibility":
        visibility_data = {key: value.get("visibility") for key, value in banners["basic_banners"].items()}
        await callback_query.message.answer("Click on the promotion to change the visibility value (Basic banners):",
                                            reply_markup=await create_toggle_visibility_kb(visibility_data, "basic_"))

    elif data == "change_selecting_section_promo_visibility":
        visibility_data = {key: value.get("visibility") for key, value in {k: v for k, v in banners.items() if k != "basic_banners"}.items()}
        await callback_query.message.answer("Click on the promotion to change the visibility value (Promo):",
                                            reply_markup=await create_toggle_visibility_kb(visibility_data,  "promo_"))

    elif data == "change_selecting_section_basic_banners_banners":
        names_array = list(banners["basic_banners"].keys())
        await callback_query.message.answer("Select offer (Basic banners):",
                                            reply_markup=await create_list_change_banners_kb(names_array,
                                                                                           "basic_"))

    elif data == "change_selecting_section_promo_banners":
        names_array = [key for key in banners.keys() if key != "basic_banners"]
        await callback_query.message.answer("Select offer (Promo):",
                                            reply_markup=await create_list_change_banners_kb(names_array,
                                                                                           "promo_"))

#Visibility
@admin_router.callback_query(lambda c: c.data.startswith('tgg_vsblt_'))
async def handle_toggle_visibility(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    banners = await get_banners()

    prefix_basic_banners = 'tgg_vsblt_basic_'
    prefix_promo = 'tgg_vsblt_promo_'



    # Проверяем наличие префиксов и извлекаем значение
    if prefix_basic_banners in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_basic_banners, 1)[1]
        key_to_update = text.replace('_', ' ')
        for category, items in banners.items():
            if isinstance(items, dict):
                if key_to_update in items:
                    # Инвертируем текущее значение 'visibility'
                    items[key_to_update]['visibility'] = not items[key_to_update]['visibility']

        visibility_data = {key: value.get("visibility") for key, value in banners["basic_banners"].items()}

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.edit_reply_markup(reply_markup=await create_toggle_visibility_kb(visibility_data, "basic_"))

    elif prefix_promo in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_promo, 1)[1]
        key_to_update = text.replace('_', ' ')

        if key_to_update in banners:
            banners[key_to_update]["visibility"] = not banners[key_to_update]["visibility"]

        visibility_data = {key: value.get("visibility") for key, value in
                           {k: v for k, v in banners.items() if k != "basic_banners"}.items()}

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.edit_reply_markup(
            reply_markup=await create_toggle_visibility_kb(visibility_data, "promo_"))

    await save_banners(banners)



#Banners

class ChangeStockBasicBanners(StatesGroup):
    stock_name = State()
    old_name = State()
    data_zip = State()
    file_info = State()

class ChangeStockPromo(StatesGroup):
    stock_name = State()
    old_name = State()
    promocode_location = State()
    confirm_data = State()
    data_zip = State()
    file_info = State()



@admin_router.callback_query(lambda c: c.data.startswith('chg_b_list_'))
async def handle_list_change_banners(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()

    prefix_basic_banners = 'chg_b_list_basic_'
    prefix_promo = 'chg_b_list_promo_'

    if prefix_basic_banners in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_basic_banners, 1)[1]
        key_to_update = text.replace('_', ' ')

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.answer(f"Offer name: {key_to_update} (Basic banners)",
                                            reply_markup=await create_change_name_offer_kb(key_to_update, "basic_"))

    elif prefix_promo in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_promo, 1)[1]
        key_to_update = text.replace('_', ' ')

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.answer(f"Offer name: {key_to_update} (Promo)",
            reply_markup=await create_change_name_offer_kb(key_to_update, "promo_"))



@admin_router.callback_query(lambda c: c.data.startswith('chg_NM_'))
async def handle_change_name_offer_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    prefix_save_basic_banners = 'chg_NM_SV_basic_'
    prefix_save_promo = 'chg_NM_SV_promo_'

    prefix_change_basic_banners = 'chg_NM_CHG_basic_'
    prefix_change_promo = 'chg_NM_CHG_promo_'

    #Basic
    if prefix_save_basic_banners in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_save_basic_banners, 1)[1]
        key_to_update = text.replace('_', ' ')
        await callback_query.message.answer("Send a zip archive with images:",
                             reply_markup=await create_change_data_zip_offer_kb(key_to_update,
                                                                                "basic_"))
        await state.set_state(ChangeStockBasicBanners.old_name)
        await state.update_data(old_name=key_to_update, stock_name=key_to_update)

    elif prefix_change_basic_banners in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_change_basic_banners, 1)[1]
        key_to_update = text.replace('_', ' ')

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.answer(f"Offer name now:{key_to_update} (Basic banners) \nPlease send the new offer name: ",
            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockBasicBanners.stock_name)
        await state.update_data(old_name=key_to_update)


    #Promo
    elif prefix_save_promo in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_save_promo, 1)[1]
        key_to_update = text.replace('_', ' ')
        await callback_query.message.answer("Location of the promo code:",
                             reply_markup=await create_change_location_promocode_kb())
        await state.set_state(ChangeStockPromo.old_name)
        await state.update_data(old_name=key_to_update, stock_name=key_to_update)


    elif prefix_change_promo in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_change_promo, 1)[1]
        key_to_update = text.replace('_', ' ')

        # Обновляем сообщение с новой клавиатурой
        await callback_query.message.answer(f"Offer name now:{key_to_update} (Pomo) \nPlease send the new offer name: ",
            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockPromo.stock_name)
        await state.update_data(old_name=key_to_update)




@admin_router.callback_query(ChangeStockBasicBanners.old_name, lambda c: c.data.startswith('chg_dzip_'))
async def handle_data_zip_offer(callback_query: types.CallbackQuery, state: FSMContext):
    banners = await get_banners()
    prefix_save_basic_banners_data_zip = 'chg_dzip_SV_basic_'
    prefix_save_promo_data_zip = 'chg_dzip_SV_promo_'

    prefix_change_basic_banners_data_zip = 'chg_dzip_CHG_basic_'
    prefix_change_promo_data_zip = 'chg_dzip_CHG_promo_'


    if prefix_save_basic_banners_data_zip in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_save_basic_banners_data_zip, 1)[1]
        old_name = text.replace('_', ' ')
        data = await state.get_data()
        stock_name = data["stock_name"]
        if old_name != stock_name:
            parent_directory = "stock_data/basic_banners"
            old_folder_path = os.path.join(parent_directory, old_name)
            new_folder_path = os.path.join(parent_directory, stock_name)

            # Проверяем, существует ли старая папка
            if os.path.exists(old_folder_path):
                # Переименовываем старую папку в новую
                os.rename(old_folder_path, new_folder_path)
                if old_name in banners.get("basic_banners", {}):
                    # Извлечь данные старого ключа
                    value = banners["basic_banners"].pop(old_name)

                    # Обновить пути в данных
                    await update_banners_list(value, old_name, stock_name)

                    # Присвоить данные новому ключу
                    banners["basic_banners"][stock_name] = value
                await callback_query.message.answer("The offer name has been successfully changed!",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await save_banners(banners)
            else:
                await callback_query.message.answer("This offer no longer exists!",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))

        else:
            await callback_query.message.answer("No changes to the offer were required!",
                                                reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
    elif prefix_change_basic_banners_data_zip in callback_query.data:
        # Извлекаем значение после префикса
        text = callback_query.data.split(prefix_change_basic_banners_data_zip, 1)[1]
        key_to_update = text.replace('_', ' ')
        old_name = text.replace('_', ' ')
        data = await state.get_data()
        stock_name = data["stock_name"]
        if old_name != stock_name:
            await callback_query.message.answer("Send a zip archive with images",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(ChangeStockBasicBanners.data_zip)
            await state.update_data(stock_name=stock_name)
            await state.update_data(old_name=old_name)
        else:

            # Обновляем сообщение с новой клавиатурой
            await callback_query.message.answer("Send a zip archive with images",
                reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(ChangeStockBasicBanners.data_zip)
            await state.update_data(stock_name=old_name)
            await state.update_data(old_name=old_name)




@admin_router.message(ChangeStockBasicBanners.stock_name, (F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def change_name_offer_basic_banners(message: types.Message, state: FSMContext):
    banners = await get_banners()
    names_array = list(banners["basic_banners"].keys())
    if message.text and message.text not in names_array:
        words = message.text.split()
        if all(re.fullmatch(r'^[A-Za-z0-9!@#$%&*()€]{1,42}$', word) for word in words):
            data = await state.get_data()
            old_name = data['old_name']
            await message.answer("Offer images:",
                                 reply_markup=await create_change_data_zip_offer_kb(old_name, "basic_"))
            await state.set_state(ChangeStockBasicBanners.old_name)
            await state.update_data(stock_name=message.text)
        else:
            await message.answer("Please enter the correct banner name(Maximum 42 characters):",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(ChangeStockBasicBanners.stock_name)
    else:
        await message.answer("This offer name already exists, enter a different one:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockBasicBanners.stock_name)




@admin_router.message(ChangeStockBasicBanners.data_zip, F.document)
async def cahnge_basic_banner_zip_file(message: types.Message, bot: Bot, state: FSMContext):
    # Проверка, что файл является ZIP архивом
    if not message.document.file_name.endswith('.zip'):
        await message.reply("Please send a ZIP archive.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockBasicBanners.data_zip)
    else:
        LANGUAGES = ['az', 'uz', 'kz', 'tr', 'ru', 'en', 'br', 'ng']
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']

        # Загрузка архива
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(file_info=file_info.file_path)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Проверка наличия файлов нужного типа в архиве
        with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(file.lower().endswith(tuple(ALLOWED_EXTENSIONS)) for file in file_list):
                await message.reply(
                    "The archive does not contain supported files (JPEG). Please send an archive with JPEG images.",
                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.set_state(ChangeStockBasicBanners.data_zip)
            else:
                # Создание уникальной временной директории для распаковки
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)

                # Распаковка ZIP-архива
                zip_ref.extractall(temp_dir)

            # Группировка файлов по языковым окончаниям
            language_groups = {}
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    for lang in LANGUAGES:
                        if file.endswith(f'_{lang}.jpg') or file.endswith(f'_{lang}.jpeg'):  # Поддерживаемые форматы
                            relative_path = os.path.relpath(os.path.join(root, file), ".")
                            if lang not in language_groups:
                                language_groups[lang] = []
                            language_groups[lang].append(relative_path)

            # Отправка файлов по группам
            for lang, files in language_groups.items():
                if files:
                    # Создание медиагруппы
                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()
                    promo_files = [file for file in files if '_promo_' in file]
                    if promo_files:
                        await process_images_and_add_text(promo_files, "TEST")

                    for file_path in files:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1/3)

            await message.answer("Add banners?", reply_markup=await confirmation_banners_kb())

            # Удаление временной директории и её содержимого
            shutil.rmtree(temp_dir)
            await state.set_state(ChangeStockBasicBanners.file_info)


@admin_router.callback_query(ChangeStockBasicBanners.file_info, lambda c: c.data.startswith('confirmation_banners_'))
async def upload_confirmation_change_banners_process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    action = callback_query.data
    banners = await get_banners()

    names_array = list(banners["basic_banners"].keys())
    if action == 'confirmation_banners_remake':
        await callback_query.message.answer("Select offer (Basic banners):",
                                            reply_markup=await create_list_change_banners_kb(names_array,
                                                                                             "basic_"))
        await state.clear()

    elif action == 'confirmation_banners_apply':
        data = await state.get_data()
        folder_path = f"stock_data/basic_banners/{data['old_name']}"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # Удаляем папку и все её содержимое
                shutil.rmtree(folder_path)
                banners["basic_banners"].pop(data['old_name'], None)
            except Exception as e:
                print(f"Не удалось удалить папку {folder_path}: {e}")
        else:
            await callback_query.message.answer("This offer no longer exists/")
            await callback_query.message.answer("Select offer (Basic banners):",
                                                reply_markup=await create_list_change_banners_kb(names_array,
                                                                                                "basic_"))
            await state.clear()

        downloaded_file = await bot.download_file(data['file_info'])
        os.makedirs(os.path.join('stock_data', 'basic_banners', data['stock_name']), exist_ok=True)

        main_folder_path = os.path.join("stock_data", "basic_banners", data['stock_name'])

        with zipfile.ZipFile(downloaded_file) as archive:
            for file_name in archive.namelist():
                if '_' in file_name:
                    # Определение типа промо
                    if '_promo_' in file_name:
                        promo_type = 'promo'
                    else:
                        promo_type = 'no_promo'

                    # Извлечение языка (после последнего '_')
                    suffix = file_name.split('_')[-1].split('.')[0]
                    language = suffix  # Язык находится в конце имени файла перед расширением

                    # Определение пути к папке для извлечения
                    folder_path = os.path.join(main_folder_path, language, promo_type)

                    # Создание папки для языка и типа промо
                    os.makedirs(folder_path, exist_ok=True)

                    # Определение имени файла без путей
                    file_name_without_path = os.path.basename(file_name)

                    # Полный путь для извлечения
                    extract_path = os.path.join(folder_path, file_name_without_path)

                    # Извлечение файла
                    with open(extract_path, 'wb') as out_file:
                        out_file.write(archive.read(file_name))
                    if data['stock_name'] not in banners['basic_banners']:
                        banners['basic_banners'][data['stock_name']] = {'visibility': True}

                    # Заполнение словаря баннеров
                    if language not in banners['basic_banners'][data['stock_name']]:
                        banners['basic_banners'][data['stock_name']][language] = {'promo': [], 'no_promo': []}

                    # Добавление пути к файлу в соответствующий массив
                    relative_path = os.path.relpath(extract_path, ".")
                    banners['basic_banners'][data['stock_name']][language][promo_type].append(relative_path)
        await state.clear()
        await save_banners(banners)
        await callback_query.message.reply(f"Promotion {data['stock_name']} successfully changed to Basic banners!",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))






#Promo

@admin_router.callback_query(ChangeStockPromo.old_name, lambda c: c.data.startswith('chg_LC_PC_'))
async def handle_confirm_location_promo_offer(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    prefix_save_promo_location = 'chg_LC_PC_SV_'
    prefix_change_promo_location = 'chg_LC_PC_CHG_'
    if prefix_save_promo_location in callback_query.data:
        await state.update_data(promocode_location=False)
        await callback_query.message.answer("Promo images:",
                                            reply_markup=await create_change_data_promo_kb())
        await state.set_state(ChangeStockPromo.confirm_data)


    elif prefix_change_promo_location in callback_query.data:
        files = ["img/bottom_left.png", "img/top_bottom.png", "img/top_cener.png"]
        await callback_query.message.answer("Example of location:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        for file_path in files:
            await bot.send_photo(chat_id=callback_query.message.chat.id, photo=FSInputFile(file_path))

        await callback_query.message.answer("Select the location of the promo code:",
                             reply_markup=await location_promocode_kb())
        await state.set_state(ChangeStockPromo.promocode_location)






@admin_router.message(ChangeStockPromo.stock_name, (F.text != "Download") & (F.text != "Upload") & (F.text != "Settings"))
async def change_name_stock_promo_banner(message: types.Message, state: FSMContext, bot: Bot):

    if message.text:
        words = message.text.split()
        if all(re.fullmatch(r'^[A-Za-z0-9!@#$%&*()€]{1,42}$', word) for word in words):
            await state.update_data(stock_name=message.text)

            await message.answer("Location of the promo code:",
                                 reply_markup=await create_change_location_promocode_kb())
            await state.set_state(ChangeStockPromo.old_name)
        else:
            await message.answer("Please enter the correct banner name(Maximum 42 characters):",
                                 reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.set_state(ChangeStockPromo.stock_name)
    else:
        await message.answer("Please enter the correct banner name:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockPromo.stock_name)


# Обработчик нажатий на кнопки выбора
@admin_router.callback_query(ChangeStockPromo.promocode_location, lambda c: c.data and c.data.startswith('location_promocode_'))
async def process__cahnge_location_promo_promocode(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data

    if "location_promocode_apply_" in data:
        selected_text = data.split("location_promocode_apply_")[1]
        await state.update_data(promocode_location=selected_text.lower())
        await callback_query.message.answer("Promo images",
                                 reply_markup=await create_change_data_promo_kb())
        await state.set_state(ChangeStockPromo.confirm_data)
    else:
        # Обновление выбора
        selected = data.replace("location_promocode_", "").replace("_", " ")
        # Обновляем клавиатуру с выбранной кнопкой
        keyboard = await location_promocode_kb(selected)
        await callback_query.message.edit_text("Please select an option:", reply_markup=keyboard)



@admin_router.callback_query(ChangeStockPromo.confirm_data, lambda c: c.data and c.data.startswith('chg_DT_ZIP_'))
async def process__cahnge_location_promo_promocode(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data
    banners = await get_banners()
    data = await state.get_data()
    location_promocode = data["promocode_location"]
    if action == "chg_DT_ZIP_SV_":
        old_name = data["old_name"]
        stock_name = data["stock_name"]
        if old_name != stock_name and location_promocode:
            parent_directory = "stock_data"
            old_folder_path = os.path.join(parent_directory, old_name)
            new_folder_path = os.path.join(parent_directory, stock_name)

            # Проверяем, существует ли старая папка
            if os.path.exists(old_folder_path):
                # Переименовываем старую папку в новую
                os.rename(old_folder_path, new_folder_path)
                if old_name in banners:
                    # Извлечь данные старого ключа
                    value = banners.pop(old_name)

                    # Обновить пути в данных
                    await update_banners_list(value, old_name, stock_name)

                    # Присвоить данные новому ключу
                    value["position_promo"] = location_promocode
                    banners[stock_name] = value
                await callback_query.message.answer("The offer name and position promo has been successfully changed!",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await save_banners(banners)
            else:
                await callback_query.message.answer("This offer no longer exists!",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))

        else:
            if old_name != stock_name:
                parent_directory = "stock_data"
                old_folder_path = os.path.join(parent_directory, old_name)
                new_folder_path = os.path.join(parent_directory, stock_name)

                # Проверяем, существует ли старая папка
                if os.path.exists(old_folder_path):
                    # Переименовываем старую папку в новую
                    os.rename(old_folder_path, new_folder_path)
                    if old_name in banners:
                        # Извлечь данные старого ключа
                        value = banners.pop(old_name)

                        # Обновить пути в данных
                        await update_banners_list(value, old_name, stock_name)

                        # Присвоить данные новому ключу
                        banners[stock_name] = value
                    await callback_query.message.answer("The offer name has been successfully changed!",
                                                        reply_markup=general_menu_admins_kb.as_markup(
                                                            resize_keyboard=True))
                    await save_banners(banners)

            else:
                if location_promocode:
                    old_name = data["old_name"]
                    banners[old_name]["position_promo"] = location_promocode
                    await save_banners(banners)

                else:
                    await callback_query.message.answer("No changes to the offer were required!",
                                                        reply_markup=general_menu_admins_kb.as_markup(
                                                            resize_keyboard=True))

    elif action == "chg_DT_ZIP_CHG_":
        if not location_promocode:
            await state.update_data(promocode_location=banners[data["old_name"]]["position_promo"])


        await callback_query.message.answer("Send a zip archive with images",
                                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockPromo.data_zip)



@admin_router.message(ChangeStockPromo.data_zip, F.document)
async def handle_change_promo_banner_zip_file(message: types.Message, bot: Bot, state: FSMContext):
    # Проверка, что файл является ZIP архивом
    if not message.document.file_name.endswith('.zip'):
        await message.reply("Please send a ZIP archive.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(ChangeStockPromo.data_zip)
    else:
        LANGUAGES = ['az', 'uz', 'kz', 'tr', 'ru', 'en', 'br', 'ng']
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']

        # Загрузка архива
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(file_info=file_info.file_path)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Проверка наличия файлов нужного типа в архиве
        with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(file.lower().endswith(tuple(ALLOWED_EXTENSIONS)) for file in file_list):
                await message.reply(
                    "The archive does not contain supported files (JPEG). Please send an archive with JPEG images.",
                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.set_state(ChangeStockPromo.data_zip)
            else:
                # Создание уникальной временной директории для распаковки
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)

                # Распаковка ZIP-архива
                zip_ref.extractall(temp_dir)

            # Группировка файлов по языковым окончаниям
            language_groups = {}
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    for lang in LANGUAGES:
                        if file.endswith(f'_{lang}.jpg') or file.endswith(f'_{lang}.jpeg'):  # Поддерживаемые форматы
                            relative_path = os.path.relpath(os.path.join(root, file), ".")
                            if lang not in language_groups:
                                language_groups[lang] = []
                            language_groups[lang].append(relative_path)

            # Отправка файлов по группам
            for lang, files in language_groups.items():
                if files:
                    # Создание медиагруппы
                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()
                    promocode_location = data_state["promocode_location"]
                    promo_files = [file for file in files if '_promo_' in file]
                    if promo_files:
                        await process_images_and_add_text(promo_files, "TEST", promocode_location)

                    for file_path in files:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1/3)

            await message.answer("Add banners?", reply_markup=await confirmation_banners_kb())

            # Удаление временной директории и её содержимого
            shutil.rmtree(temp_dir)
            await state.set_state(ChangeStockPromo.file_info)


@admin_router.callback_query(ChangeStockPromo.file_info, lambda c: c.data.startswith('confirmation_banners_'))
async def change_confirmation_promo_banners_process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    action = callback_query.data
    banners = await get_banners()
    names_array = [key for key in banners.keys() if key != "basic_banners"]
    if action == 'confirmation_banners_remake':
        await callback_query.message.answer("Select offer (Promo):",
                                            reply_markup=await create_list_change_banners_kb(names_array,
                                                                                             "promo_"))
        await state.clear()
    elif action == 'confirmation_banners_apply':
        data = await state.get_data()
        folder_path = f"stock_data/{data['old_name']}"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # Удаляем папку и все её содержимое
                shutil.rmtree(folder_path)
                banners.pop(data['old_name'], None)
            except Exception as e:
                print(f"Не удалось удалить папку {folder_path}: {e}")
        else:
            await callback_query.message.answer("This offer no longer exists/")
            await callback_query.message.answer("Select offer (Promo):",
                                                reply_markup=await create_list_change_banners_kb(names_array,
                                                                                                 "promo_"))
            await state.clear()



        downloaded_file = await bot.download_file(data['file_info'])
        os.makedirs(os.path.join('stock_data', data['stock_name']), exist_ok=True)

        main_folder_path = os.path.join("stock_data", data['stock_name'])

        with zipfile.ZipFile(downloaded_file) as archive:
            for file_name in archive.namelist():
                if '_' in file_name:
                    # Определение типа промо
                    if '_promo_' in file_name:
                        promo_type = 'promo'
                    else:
                        promo_type = 'no_promo'

                    # Извлечение языка (после последнего '_')
                    suffix = file_name.split('_')[-1].split('.')[0]
                    language = suffix  # Язык находится в конце имени файла перед расширением

                    # Определение пути к папке для извлечения
                    folder_path = os.path.join(main_folder_path, language, promo_type)

                    # Создание папки для языка и типа промо
                    os.makedirs(folder_path, exist_ok=True)

                    # Определение имени файла без путей
                    file_name_without_path = os.path.basename(file_name)

                    # Полный путь для извлечения
                    extract_path = os.path.join(folder_path, file_name_without_path)

                    # Извлечение файла
                    with open(extract_path, 'wb') as out_file:
                        out_file.write(archive.read(file_name))
                    if data['stock_name'] not in banners:
                        banners[data['stock_name']] = {'visibility': True, 'position_promo': data['promocode_location']}

                    # Заполнение словаря баннеров
                    if language not in banners[data['stock_name']]:
                        banners[data['stock_name']][language] = {'promo': [], 'no_promo': []}

                    # Добавление пути к файлу в соответствующий массив
                    relative_path = os.path.relpath(extract_path, ".")
                    banners[data['stock_name']][language][promo_type].append(relative_path)
        await state.clear()
        await save_banners(banners)
        await callback_query.message.reply(f"Promotion {data['stock_name']}  successfully changed to Promo!",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))




#Delete

class DeleteOffer(StatesGroup):
    name_offer = State()
    confirm_remove = State()

@admin_router.callback_query(lambda c: c.data and c.data.startswith('del_'))
async def delete_offer_section(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    banners = await get_banners()
    action = callback_query.data
    if action == "del_basic_":
        names_array = list(banners["basic_banners"].keys())
        await callback_query.message.answer("Select offer (Basic banners):",
                                           reply_markup=await create_del_list_offer_kb(names_array, "basic_"))

    elif action == "del_promo_":
        names_array = [key for key in banners.keys() if key != "basic_banners"]
        await callback_query.message.answer("Select offer (Basic banners):",
                                           reply_markup=await create_del_list_offer_kb(names_array, "promo_"))



@admin_router.callback_query(lambda c: c.data and c.data.startswith('remove_'))
async def remove_offer_to_name(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    banners = await get_banners()
    prefix_remove_basic_banners = "remove_basic_"
    prefix_remove_promo = "remove_promo_"

    if prefix_remove_basic_banners in callback_query.data:
        text = callback_query.data.split(prefix_remove_basic_banners, 1)[1]
        key_to_remove = text.replace('_', ' ')
        await callback_query.message.answer(f"{key_to_remove} (Basic banners)")
        if key_to_remove in banners['basic_banners']:
            banner_info = banners['basic_banners'][key_to_remove]

            # Сбор путей к картинкам по языкам
            for lang, data in banner_info.items():
                if isinstance(data, dict):  # Проверяем, что данные по языку
                    promo_paths = data.get("promo", [])
                    no_promo_paths = data.get("no_promo", [])

                    temp_dir = os.path.join(".", f"temp_{callback_query.message.chat.id}")
                    promo_dir = os.path.join(temp_dir, "promo")
                    no_promo_dir = os.path.join(temp_dir, "no_promo")

                    os.makedirs(promo_dir, exist_ok=True)
                    os.makedirs(no_promo_dir, exist_ok=True)

                    # Копирование файлов в соответствующие директории и сохранение их путей
                    all_temp_paths = []  # Массив для всех путей (promo + no_promo)
                    promo_temp_paths = []  # Массив только для путей promo

                    # Копирование файлов promo и сохранение их путей
                    for path in promo_paths:
                        if os.path.exists(path):
                            dest_path = shutil.copy(path, promo_dir)
                            promo_temp_paths.append(dest_path)
                            all_temp_paths.append(dest_path)
                        else:
                            print(f"Файл {path} не найден.")

                    # Копирование файлов no_promo и сохранение их путей
                    for path in no_promo_paths:
                        if os.path.exists(path):
                            dest_path = shutil.copy(path, no_promo_dir)
                            all_temp_paths.append(dest_path)
                        else:
                            print(f"Файл {path} не найден.")

                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()

                    await process_images_and_add_text(promo_temp_paths, "TEST")

                    for file_path in all_temp_paths:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=callback_query.message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1 / 3)
                    shutil.rmtree(temp_dir)
            await callback_query.message.answer("Banners deleted? (Basic banners)",
                                                reply_markup=await create_remove_apply_kb("basic_"))
            await state.set_state(DeleteOffer.confirm_remove)
            await state.update_data(name_offer=key_to_remove)
        else:
            await callback_query.message.answer("There is no such offer. (Basic banners)",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.clear()





    elif prefix_remove_promo in callback_query.data:
        text = callback_query.data.split(prefix_remove_promo, 1)[1]
        key_to_remove = text.replace('_', ' ')
        await callback_query.message.answer(f"{key_to_remove} (Promo)")
        if key_to_remove in banners:
            banner_info = banners[key_to_remove]

            # Получение позиции промо
            position_promo = banner_info.get("position_promo", "Позиция не указана")
            print("Позиция промо:", position_promo)

            # Сбор путей к картинкам по языкам
            for lang, data in banner_info.items():
                if lang not in ["visibility", "position_promo"] and isinstance(data, dict):
                    promo_paths = data.get("promo", [])
                    no_promo_paths = data.get("no_promo", [])

                    temp_dir = os.path.join(".", f"temp_{callback_query.message.chat.id}")
                    promo_dir = os.path.join(temp_dir, "promo")
                    no_promo_dir = os.path.join(temp_dir, "no_promo")

                    os.makedirs(promo_dir, exist_ok=True)
                    os.makedirs(no_promo_dir, exist_ok=True)

                    # Копирование файлов в соответствующие директории и сохранение их путей
                    all_temp_paths = []  # Массив для всех путей (promo + no_promo)
                    promo_temp_paths = []  # Массив только для путей promo

                    # Копирование файлов promo и сохранение их путей
                    for path in promo_paths:
                        if os.path.exists(path):
                            dest_path = shutil.copy(path, promo_dir)
                            promo_temp_paths.append(dest_path)
                            all_temp_paths.append(dest_path)
                        else:
                            print(f"Файл {path} не найден.")

                    # Копирование файлов no_promo и сохранение их путей
                    for path in no_promo_paths:
                        if os.path.exists(path):
                            dest_path = shutil.copy(path, no_promo_dir)
                            all_temp_paths.append(dest_path)
                        else:
                            print(f"Файл {path} не найден.")

                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()

                    await process_images_and_add_text(promo_temp_paths, "TEST", position_promo)

                    for file_path in all_temp_paths:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=callback_query.message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1 / 3)
                    shutil.rmtree(temp_dir)
            await callback_query.message.answer("Banners deleted? (Promo)",
                                                reply_markup=await create_remove_apply_kb("promo_"))
            await state.set_state(DeleteOffer.confirm_remove)
            await state.update_data(name_offer=key_to_remove)

        else:
            await callback_query.message.answer("There is no such offer. (Promo)",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.clear()


@admin_router.callback_query(DeleteOffer.confirm_remove, lambda c: c.data and c.data.startswith('apply_del_'))
async def remove_offer_process(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    banners = await get_banners()
    data = await state.get_data()
    if callback_query.data == "apply_del_basic_":
        folder_path = f"stock_data/basic_banners/{data['name_offer']}"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # Удаляем папку и все её содержимое
                shutil.rmtree(folder_path)
                banners["basic_banners"].pop(data['name_offer'], None)
                await save_banners(banners)
                await callback_query.message.answer(f"Banners {data['name_offer']} deleted! (Basic banners)",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.clear()
            except Exception as e:
                print(f"Не удалось удалить папку {folder_path}: {e}")
        else:
            await callback_query.message.answer("This offer no longer exists",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.clear()
    elif callback_query.data == "apply_del_promo_":
        folder_path = f"stock_data/{data['name_offer']}"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # Удаляем папку и все её содержимое
                shutil.rmtree(folder_path)
                banners.pop(data['name_offer'], None)
                await callback_query.message.answer(f"Banners {data['name_offer']} deleted! (Promo)",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await save_banners(banners)
                await state.clear()
            except Exception as e:
                print(f"Не удалось удалить папку {folder_path}: {e}")
        else:
            await callback_query.message.answer("This offer no longer exists",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
            await state.clear()

    else:
        await callback_query.message.answer("Сhanges cancelled",
                                                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.clear()
