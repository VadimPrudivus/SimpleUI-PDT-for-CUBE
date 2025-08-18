import json

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")
    if message:
        data = json.loads(message)  # Преобразуем JSON строку в словарь
        # Записываем в стек переменных SimpleUI
        hashMap.put("user_id", data.get("id", ""))
        hashMap.put("user_name", data.get("name", ""))
        # Можно вернуть сообщение или просто выйти
