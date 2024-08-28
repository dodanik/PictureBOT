import ujson

with open("json_data_file/botlang.json", "r") as jsonlng:
    botlang_json = ujson.load(jsonlng)

with open("json_data_file/banners.json", "r") as jsonbanners:
    banners = ujson.load(jsonbanners)

botlang = {}
for key, value in botlang_json.items():
    botlang[int(key)] = value


async def save_botlang(data):
    global botlang
    botlang = data


async def get_botlang():
    global botlang
    return botlang




async def save_local_botlang():
    global botlang
    with open("json_data_file/botlang.json", "w") as botlang_file:
        ujson.dump(botlang, botlang_file)






async def save_banners(data):
    global banners
    banners = data
    with open("json_data_file/banners.json", "w") as banners_file:
        ujson.dump(banners, banners_file)

async def get_banners():
    global banners
    return banners
