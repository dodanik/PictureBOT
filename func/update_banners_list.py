async def update_banners_list(d, old_name, new_name):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, str):
                d[k] = v.replace(old_name, new_name)
            elif isinstance(v, list):
                # Поскольку замена строк не требует асинхронности,
                # делаем её в обычном режиме
                d[k] = [x.replace(old_name, new_name) for x in v]
            elif isinstance(v, dict):
                await update_banners_list(v, old_name, new_name)
    elif isinstance(d, list):
        for i in range(len(d)):
            if isinstance(d[i], str):
                d[i] = d[i].replace(old_name, new_name)
            elif isinstance(d[i], dict):
                await update_banners_list(d[i], old_name, new_name)