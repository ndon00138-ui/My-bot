from http.server import BaseHTTPRequestHandler
import json
import requests

TOKEN = "8348577528:AAEsJ_g7dGOoPV4PmSucGhJTZGQCU5c56V4" # သင့် Token ကို အမှန်ပြန်ထည့်ပါ

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                reply = "မင်္ဂလာပါ။ Calculator Bot ပါ။ သင်္ချာပုစ္ဆာ ပို့လိုက်ပါ (ဥပမာ- 5x5 သို့မဟုတ် 10*2)။"
            else:
                try:
                    # User ရိုက်လိုက်တဲ့ 'x' သို့မဟုတ် '×' ကို '*' အဖြစ် ပြောင်းပေးခြင်း
                    formula = text.replace('x', '*').replace('×', '*').replace('÷', '/')
                    
                    # တွက်ချက်ခြင်း
                    result = eval(formula)
                    reply = f"တွက်ချက်မှုရလဒ်မှာ: {result} ဖြစ်ပါတယ်"
                except:
                    reply = "မှားယွင်းနေပါတယ်။ ဂဏန်းနဲ့ သင်္ကေတတွေကိုပဲ သုံးပေးပါ (ဥပမာ- +, -, x, /)။"

            # အဖြေပြန်ပို့ခြင်း
            payload = {"chat_id": chat_id, "text": reply}
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
