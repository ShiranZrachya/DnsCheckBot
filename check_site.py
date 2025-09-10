import os
TO_WHATSAPP = os.getenv("TO_WHATSAPP") # e.g. +1234567890 (international format)


# Basic validation
if not PHONE_NUMBER_ID or not ACCESS_TOKEN or not TO_WHATSAPP:
print("Missing required environment variables. Make sure PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN and TO_WHATSAPP are set.")
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
body = resp.text
return resp.status_code, body
except requests.exceptions.RequestException as e:
return None, str(e)




if __name__ == "__main__":
ok, status_code, error = check_site()


if ok and status_code == 200:
print(f"OK: {WEBSITE_URL} returned 200")
sys.exit(0)


# Construct message depending on the result
if ok and status_code is not None:
message = f"🚨 Website Alert: {WEBSITE_URL} is DOWN — HTTP status {status_code}."
else:
message = f"🚨 Website Alert: {WEBSITE_URL} appears DOWN — network error: {error}"


print("=== WEBSITE ALERT (test mode) ===")
print(message)
if ok and status_code is not None:
    print(f"(HTTP status returned by check: {status_code})")
else:
    print(f"(Network error during check: {error})")


# Exit with non-zero so CI shows failure (optional)
sys.exit(1)
