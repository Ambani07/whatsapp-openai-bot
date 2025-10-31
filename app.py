from flask import Flask, request
import requests, os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GREEN_ID = os.getenv("GREEN_API_ID")
GREEN_TOKEN = os.getenv("GREEN_API_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "🤖 WhatsApp + OpenAI bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        msg = data["messageData"]["textMessageData"]["textMessage"]
        chat_id = data["senderData"]["chatId"]
    except KeyError:
        return "no message", 200

    # --- Call OpenAI ---
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful WhatsApp assistant."},
            {"role": "user", "content": msg}
        ],
        "max_tokens": 150
    }
    r = requests.post("https://api.openai.com/v1/chat/completions",
                      headers=headers, json=payload)
    reply = r.json()["choices"][0]["message"]["content"]

    # --- Send reply via Green-API ---
    send_url = f"https://api.green-api.com/waInstance{GREEN_ID}/SendMessage/{GREEN_TOKEN}"
    requests.post(send_url, json={"chatId": chat_id, "message": reply})

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
