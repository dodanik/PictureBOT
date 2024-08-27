import io

import aiofiles
from PIL import Image, ImageDraw, ImageFont


font_path = 'fonts/TTSquaresCondensed-BlackItalic.ttf'
text_color = (255, 0, 0)
font_size = 40


async def process_images_and_add_text(image_paths, text, position):
    for image_path in image_paths:
        # Открываем изображение
        with Image.open(image_path) as image:
            # Создаем объект для рисования на изображении
            draw = ImageDraw.Draw(image)

            # Определяем шрифт
            font = ImageFont.truetype(font_path, font_size)

            # Добавляем текст
            draw.text(position, text, font=font, fill=text_color)

            # Сохраняем измененное изображение по тому же пути
            image.save(image_path, format='JPEG', quality=100, optimize=True, progressive=True)

