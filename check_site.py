import os
import sys
import requests

# Environment variables
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")  # e.g. +1234567890 (international format)
WEBSITE_URL = os.getenv("WEBSITE_URL")  # e.g. https://example.com

# Basic validation
if not PHONE_NUMBER_ID or not ACCESS_TOKEN or not TO_WHATSAPP or not WEBSITE_URL:
    print("Missing required environment variables. Make sure PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN, TO_WHATSAPP, and WEBSITE_URL are set.")
    sys.exit(2)

TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))


def check_site():
    try:
        r = requests.get(WEBSITE_URL, timeout=TIMEOUT)
        return True, r.status_code, None
    except requests.exceptions.RequestException as e:
        # network-level failure or DNS failure etc.
        return False, None, str(e)


def send_whatsapp(message_text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": TO_WHATSAPP,
        "type": "text",
        "text": {"body": message_text}
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        try:
            body = resp.json()
        except Exception:
