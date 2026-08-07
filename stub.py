import os
import json
import time
import urllib.request

# Берем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("Ошибка: BOT_TOKEN не найден!")
    exit(1)

API_URL = f"https://api.telegram.org/bot{TOKEN}/"
offset = 0

print("🛠 Бот-заглушка запущен. Отвечаем пользователям...")

while True:
    try:
        # Получаем новые сообщения
        req = urllib.request.Request(API_URL + f"getUpdates?offset={offset}&timeout=10")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                
                # Если это обычное сообщение
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    
                    # Отправляем ответ о техобслуживании
                    send_url = API_URL + "sendMessage"
                    payload = json.dumps({
                        "chat_id": chat_id, 
                        "text": "🛠 <b>Техническое обслуживание!</b>\n\nБот обновляется и скоро вернется в строй. Пожалуйста, подождите немного.",
                        "parse_mode": "HTML"
                    }).encode()
                    
                    headers = {"Content-Type": "application/json"}
                    req_send = urllib.request.Request(send_url, data=payload, headers=headers)
                    urllib.request.urlopen(req_send)
                    
    except Exception as e:
        # В случае ошибки сети просто ждем и пробуем снова
        time.sleep(1)