import json

def ws_handler(hashMap, _files=None, _data=None):
    if not hashMap:
        # хэндлить случай с пустым hashMap, чтобы не обращаться к None
        return

    message = hashMap.get("WebSocketMessage")
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
        #hashMap.put("user_id", data.get("id", ""))
        #hashMap.put("user_name", data.get("name", ""))
        # Можно вернуть сообщение или просто выйти
