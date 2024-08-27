import ujson

with open("json_data_file/botlang.json", "r") as jsonlng:
    botlang_json = ujson.load(jsonlng)

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
