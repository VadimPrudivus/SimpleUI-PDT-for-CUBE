import json

def ws_connect(hashMap, _files=None, _data=None):
    return hashMap # пока просто ничего не делаем

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")
    hashMap.put("toast", "New "+message)

    if message:
        data = json.loads(message)
        hashMap.put("toast", str(data))

        # Проверяем, что это событие входа
        if data.get("event") == "login":
            hashMap.put("user_id", data.get("id", ""))
            hashMap.put("user_name", data.get("name", ""))

            hashMap.put("toast", hashMap.get("user_name"))
    else:
        hashMap.put("toast", "Сообщение WebSocketMessage отсутствует или пусто")

    #hashMap.put("RefreshScreen", "")

    return hashMap
