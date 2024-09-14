import io

import aiofiles
from PIL import Image, ImageDraw, ImageFont


font_path = 'fonts/TTSquaresCondensed-BlackItalic.ttf'
text_color = (255, 255, 255)
max_width = 415
min_font_size = 5


async def process_images_and_add_text(image_paths, text, position=False):
    if not position:
        position = (540, 965)
    elif position == "bottom_center":
        position = (300, 200)
    elif position == "top_center":
        position = (150, 150)
    elif position == "left_bottom":
        position = (30, 100)

    for image_path in image_paths:
        # Открываем изображение
        with Image.open(image_path) as image:
            # Создаем объект для рисования на изображении
            draw = ImageDraw.Draw(image)

            # Начальный размер шрифта
            font_size = 90

            while True:
                # Определяем шрифт
                font = ImageFont.truetype(font_path, font_size)

                # Получаем метрики шрифта (асцент и десцент)
                ascent, descent = font.getmetrics()

                # Получаем размер текста (ширина и высота с учетом десцента)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]

                if text_width <= max_width:
                    break

                # Уменьшаем размер шрифта
                font_size -= 1

                # Проверяем, чтобы размер шрифта не стал слишком маленьким
                if font_size <= min_font_size:
                    print(f"Текст не помещается даже при минимальном размере шрифта.")
                    break

            # Пересчитываем размеры текста с финальным размером шрифта
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]

            # Высота текста без нижних хвостиков
            text_height = ascent

            # Корректируем позицию для центрирования текста
            centered_position = (position[0] - text_width // 2, position[1] - text_height // 2)

            # Добавляем текст
            draw.text(centered_position, text, font=font, fill=text_color)

            # Сохраняем измененное изображение по тому же пути
            image.save(image_path, format='JPEG', quality=100, optimize=True, progressive=True)

