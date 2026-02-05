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
                reply = "မင်္ဂလာပါ။ ကျွန်တော်က Calculator Bot ပါ။ သင်္ချာပုစ္ဆာတစ်ခုခု ပို့လိုက်ပါ (ဥပမာ- 5+5)။"
            else:
                try:
                    # eval() က စာသားထဲက သင်္ချာပုစ္ဆာကို တွက်ချက်ပေးပါတယ်
                    # ဘေးကင်းအောင် ဂဏန်းနဲ့ သင်္ချာသင်္ကေတပဲ ပါတာကို စစ်ဆေးတာမျိုး လုပ်သင့်ပါတယ်
                    result = eval(text)
                    reply = f"တွက်ချက်မှုရလဒ်မှာ: {result} ဖြစ်ပါတယ်"
                except:
                    reply = "မှားယွင်းနေပါတယ်။ ဂဏန်းနဲ့ သင်္ကေတတွေကိုပဲ သုံးပေးပါ (ဥပမာ- +, -, *, /)။"

            # အဖြေပြန်ပို့ခြင်း
            payload = {"chat_id": chat_id, "text": reply}
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
