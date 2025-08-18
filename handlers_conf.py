def ws_handler(hashMap, _files=None, _data=None):
    import json
    message = hashMap.get("WebSocketMessage")
    data = json.loads(message)

    # Флаг, показывающий нужно ли отправлять ответ
    send_response = (data.get("event")!= "response_from_ui")

    if send_response:
        response = {"event": "response_from_ui", "received": data}
        hashMap.put("WebSocketSend", json.dumps(response))

    return hashMap
