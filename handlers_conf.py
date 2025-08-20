import json

def ws_connect(hashMap, _files=None, _data=None):
    return hashMap # пока просто ничего не делаем

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")
    #hashMap.put("toast", "New "+message)

    if message:
        data = json.loads(message)
        #hashMap.put("toast", str(data))

        # Проверяем, что это событие входа
        if data.get("event") == "login":
            id = int(data.get("user_id", "0"))
            hashMap.put("barcode", data.get("barcode", ""))
            hashMap.put("user_id", data.get("user_id", 0))
            hashMap.put("user_name", data.get("user_name", ""))
            hashMap.put("toast", hashMap.get("user_name"))
            if id:
                hashMap.put("toast","LoginSucsess")
                hashMap.put("ShowScreen","LoginSucsess")
            else:
                hashMap.put("ShowScreen", "LoginError")    
    else:
        hashMap.put("toast", "Сообщение WebSocketMessage отсутствует или пусто")

    hashMap.put("RefreshScreen", "True")

    return hashMap
