from http.server import BaseHTTPRequestHandler
import json
import requests

# ⚠️ ဒီနေရာမှာ သင့် Bot Token ကို အတိအကျ ပြောင်းထည့်ပါ
TOKEN = "8348577528:AAEsJ_g7dGOoPV4PmSucGhJTZGQCU5c56V4" 

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            if "message" in data:
                chat_id = data["message"]["chat"]["id"]
                user_text = data["message"].get("text", "")

                # User ဆီ ပြန်စာပို့မည့်အပိုင်း
                reply_text = f"မင်္ဂလာပါ! သင်ပို့လိုက်တဲ့စာက - {user_text}"
                payload = {"chat_id": chat_id, "text": reply_text}
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
        except Exception as e:
            print(f"Error: {e}")

        # Vercel ကို အဆင်ပြေကြောင်း အကြောင်းပြန်ခြင်း
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
