import ujson

with open("json_data_file/botlang.json", "r") as jsonlng:
    botlang_json = ujson.load(jsonlng)

with open("json_data_file/banners.json", "r") as jsonbanners:
    banners = ujson.load(jsonbanners)

with open("json_data_file/admin_name_list.json", "r") as json_admin_name_list:
    admin_name_list_json = ujson.load(json_admin_name_list)


botlang = {}
for key, value in botlang_json.items():
    botlang[int(key)] = value

admin_name_list = {}
for key, value in admin_name_list_json.items():
    admin_name_list[int(key)] = value

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


async def get_admin_name_list():
    global admin_name_list
    return admin_name_list

async def save_admin_name_list(new_admin_name_list):
    global admin_name_list
    admin_name_list = new_admin_name_list
    with open("json_data_file/admin_name_list.json", "w") as admin_name_list_file:
        ujson.dump(admin_name_list, admin_name_list_file)



async def save_banners(data):
    global banners
    banners = data
    with open("json_data_file/banners.json", "w") as banners_file:
        ujson.dump(banners, banners_file)

async def get_banners():
    global banners
    return banners
