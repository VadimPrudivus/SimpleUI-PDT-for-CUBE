import json

def ws_handler(hashMap, _files=None, _data=None):
    message = hashMap.get("WebSocketMessage")
    data = json.loads(message)

    toast(message)
