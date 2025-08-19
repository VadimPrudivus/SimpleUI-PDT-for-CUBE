from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import pymssql

# Параметры подключения (можно в отдельные переменные или словарь)
db_config = {
    'server': 'testserver2',
    'user': 'prudivus',
    'password': '123',
    'database': 'automall',
    'charset':'CP1251'
}


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
            elif msg['event'] == 'login':
                barcode = msg.get('barcode')
                try:
                    print(f"Обработка login: {barcode}")
                    user_info = self.get_user_by_badge(barcode)
                    print(f"user_info из БД: {user_info}")

                    if user_info:
                        response = {
                            "event": "login",          # добавляем событие
                            "barcode": barcode,
                            "user_id": user_info.get("UserId"),
                            "user_name": user_info.get("UserFIO")
                        }
                    else:
                        response = {
                            "event": "login", # тоже отметка события
                            "barcode": barcode,
                            "user_id": 0,
                            "user_name": "User not found" # сообщение об ошибке
                        }
                    self.sendMessage(json.dumps(response, ensure_ascii=False))
                except Exception as e:
                    print(f"Ошибка при обработке login: {e}")
                    self.sendMessage(json.dumps({"error": "Internal server error"}))
            else:
                self.sendMessage(json.dumps({"error": "Unknown event"}))
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

    def get_user_by_badge(self, barcode):
        try:
            with pymssql.connect(**db_config) as conn:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.execute("EXEC tsd_GetUserByBadgeBarCode @TsdBadgeBarCode = %s", (barcode,))
                    row = cursor.fetchone()
                    if not row:
                        return None
                    print(f"User data retrieved: {row}")  # row уже словарь с нормальными строковыми ключами
                    return row
        except Exception as e:
            print(f"DB error in get_user_by_badge: {e}")
            return None

    def exec_proc(self, proc_name, params_dict):
        sql_parts = []
        params = []
        for key, val in params_dict.items():
            sql_parts.append(f"@{key} =?")
            params.append(val)

        sql = f"EXEC {proc_name} " + ", ".join(sql_parts)

        with pymssql.connect(**db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            columns = [col for col in cursor.description]
            rows = cursor.fetchall()

            result = [dict(zip(columns, row)) for row in rows]
            self.hashMap.put("SP_Result_JSON", json.dumps(result))

if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8765, SimpleBusHandler)
    print("SimpleBus server started on ws://0.0.0.0:8765")
    server.serveforever()
