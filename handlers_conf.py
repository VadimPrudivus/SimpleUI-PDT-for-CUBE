import json

def ws_connect(hashMap, _files=None, _data=None):
    return hashMap # пока просто ничего не делаем

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")

    if message:
        try:
            data = json.loads(message)
            hashMap.put("toast", data)

            # Проверяем, что это событие входа
            if data.get("event") == "login":
                hashMap.put("user_id", data.get("id", ""))
                hashMap.put("user_name", data.get("name", ""))
        
        except Exception as ex:
            # Логируем ошибку парсинга JSON
            print(f"Ошибка JSON: {ex}")
    else:
        print("Сообщение WebSocketMessage отсутствует или пусто")

    hashMap.put("RefreshScreen", "")

    return hashMap
