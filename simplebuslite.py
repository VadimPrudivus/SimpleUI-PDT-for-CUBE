from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import pyodbc

# Настройка соединения — один раз при загрузке модуля
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=testserver2;"
    "DATABASE=automall;"
    "UID=prudivus;"
    "PWD=123"
)

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
            
            user_info = self.get_user_by_badge(barcode)

            if user_info:
                self.sendMessage(json.dumps({
                    "login": barcode,
                    "id": user_info.get("UserId"),
                    "name": user_info.get("UserFIO"),
                    "FilId": user_info.get("FilId"),
                    "FilName": user_info.get("FilName"),
                    "WorkModeId": user_info.get("WorkModeId"),
                    "WorkModeName": user_info.get("WorkModeName"),
                    "CanDeclineTask": user_info.get("CanDeclineTask")
                }))
            else:
                self.sendMessage(json.dumps({"error": "User not found"}))
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
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("EXEC tsd_GetUserByBadgeBarCode @TsdBadgeBarCode =?", (barcode,))
            row = cursor.fetchone()
            if row:
                columns = [column for column in cursor.description]
                user_data = dict(zip(columns, row))
                # Формируем удобный словарь с нужными полями
                return {
                    "id": user_data.get("UserId"),
                    "name": user_data.get("UserFIO"),
                    "FilId": user_data.get("FilId"),
                    "FilName": user_data.get("FilName"),
                    "WorkModeId": user_data.get("WorkModeId"),
                    "WorkModeName": user_data.get("WorkModeName"),
                    "CanDeclineTask": user_data.get("CanDeclineTask")
                }
            else:
                return None

    def exec_proc(self, proc_name, params_dict):
        sql_parts = []
        params = []
        for key, val in params_dict.items():
            sql_parts.append(f"@{key} =?")
            params.append(val)

        sql = f"EXEC {proc_name} " + ", ".join(sql_parts)

        with pyodbc.connect(self.conn_str) as conn:
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
