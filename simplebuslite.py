from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

db = {}  # Простая БД в памяти

class SimpleBusHandler(WebSocket):
    def handleMessage(self):
        print(f"Received message from {self.address}: {self.data}")  # Выводим сырое сообщение

        try:
            msg = json.loads(self.data)
        except Exception:
            self.sendMessage(json.dumps({"error": "Invalid JSON"}))
            return

        # Простой handshake + echo команд SimpleUI
        if 'event' in msg:
            if msg['event'] == 'simplebus_get_state':
                # SimpleUI просит текущее состояние — отправляем все переменные
                self.sendMessage(json.dumps({
                    "event": "simplebus_state",
                    "variables": db
                }))
            elif msg['event'] == 'simplebus_set_var':
                # SimpleUI меняет переменную
                var = msg.get('variable')
                value = msg.get('value')
                if var:
                    db[var] = value
                    self.sendMessage(json.dumps({
                        "event": "simplebus_var_changed",
                        "variable": var,
                        "value": value
                    }))
            else:
                self.sendMessage(json.dumps({"error": "Unknown event"}))
        elif 'login' in msg:
            barcode = msg['login']
            #if barcode:
            self.sendMessage(json.dumps({
                    "login": barcode,
                    "name": "User" + barcode,
                    "id": "156"
                }))
        else:
            self.sendMessage(json.dumps({"error": "No event field"}))

    def handleConnected(self):
        print(f"Client connected: {self.address}")
        # При подключении сразу отправляем пустое состояние, чтобы SimpleUI “увидела” SimpleBus
        self.sendMessage(json.dumps({
            "event": "simplebus_state",
            "variables": db
        }))

    def handleClose(self):
        print(f"Client disconnected: {self.address}")

if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8765, SimpleBusHandler)
    print("SimpleBus server started on ws://0.0.0.0:8765")
    server.serveforever()
