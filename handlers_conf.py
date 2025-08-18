def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")
    toast(message)

    # Можно изменить hashMap, например отправить ответ:
    #hashMap.put("WebSocketSend", '{"event":"response_from_ui"}')
    #return hashMap
