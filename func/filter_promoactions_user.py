async def get_keys_with_visibility(data, lang):
    # Проверка visibility и наличия языка в одном месте
    async def check_key(key, value):
        if key != "basic_banners" and isinstance(value, dict):
            if value.get("visibility") and lang in value:
                return key
        return None

    # Получение всех ключей, удовлетворяющих условиям
    results = [
        await check_key(key, value) for key, value in data.items()
    ]

    # Возвращение всех ключей, которые удовлетворяют условиям
    return [result for result in results if result is not None]
