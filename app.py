import requests
import time
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GREEN_ID = os.getenv("GREEN_API_ID")
GREEN_TOKEN = os.getenv("GREEN_API_TOKEN")
BASE_URL = f"https://7107.api.green-api.com/waInstance{GREEN_ID}"

def get_message():
    url = f"{BASE_URL}/receiveNotification/{GREEN_TOKEN}"
    res = requests.get(url)
    message = res.json()
    return message.text

def delete_message(receipt_id):
    url = f"{BASE_URL}/deleteNotification/{GREEN_TOKEN}/{receipt_id}"
    requests.delete(url)

def send_message(chat_id, text):
    url = f"{BASE_URL}/SendMessage/{GREEN_TOKEN}"
    requests.post(url, json={"chatId": chat_id, "message": text})

def ask_openai(prompt):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }
    r = requests.post("https://api.openai.com/v1/chat/completions",
                      headers=headers, json=payload)
    return r.json()["choices"][0]["message"]["content"]

while True:
    msg = get_message()
    if msg and "body" in msg:
        try:
            receipt_id = msg["receiptId"]
            text = msg["body"]["messageData"]["textMessageData"]["textMessage"]
            chat_id = msg["body"]["senderData"]["chatId"]

            print("Received:", text)
            reply = ask_openai(text)
            send_message(chat_id, reply)
            print("Replied:", reply)

            delete_message(receipt_id)
        except Exception as e:
            print("Error:", e)
    time.sleep(5)  # check every 5 seconds
