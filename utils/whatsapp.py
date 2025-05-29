import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read from .env file
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

def send_order_confirmation(name, phone, order_id, delivery_date, delivery_time):
    if not all([PHONE_NUMBER_ID, ACCESS_TOKEN]):
        print("❌ Environment variables missing. Check .env file.")
        return False

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone.replace("+", ""),
        "type": "template",
        "template": {
            "name": "order_confirmation",
            "language": { "code": "en_US" },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        { "type": "text", "text": name },
                        { "type": "text", "text": order_id },
                        { "type": "text", "text": delivery_date },
                        { "type": "text", "text": delivery_time }
                    ]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print("📤 Payload Sent:", json.dumps(payload, indent=2))
        print("📥 Response:", response.status_code, response.text)

        if response.status_code == 200 and "messages" in response.json():
            print("✅ WhatsApp message sent successfully.")
            return True
        else:
            print("❌ WhatsApp message failed.")
            return False

    except Exception as e:
        print("❗ Exception occurred while sending WhatsApp message:", str(e))
        return False
