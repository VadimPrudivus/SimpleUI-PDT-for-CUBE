import json

def ws_connect(hashMap, _files=None, _data=None):
    return hashMap # пока просто ничего не делаем

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")

    toast(message)
    
    if message:
        try:
            data = json.loads(message)
            # дальше работа с data
        except Exception as ex:
            # Логируем ошибку парсинга JSON
            print(f"Ошибка JSON: {ex}")
    else:
        print("Сообщение WebSocketMessage отсутствует или пусто")

    # Записываем в стек переменных SimpleUI
    hashMap.put("user_id", data.get("id", ""))
    hashMap.put("user_name", data.get("name", ""))

    hashMap.put("ReloadScreen", True)

    return hashMap
