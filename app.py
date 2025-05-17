from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import time

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Raw data:", request.data)
        print("Is JSON:", request.is_json)

        data = request.get_json(force=True)
        print("DATA RECEIVED:", data)

        if not data:
            print("⚠️ No JSON received.")
            return jsonify({"error": "Invalid or empty request body"}), 400

        user_message = data.get("message")
        print("USER MESSAGE:", user_message)

        if not user_message:
            print("⚠️ No message field received.")
            return jsonify({"error": "No message provided"}), 400

        print("⏳ Sending message to OpenAI...")
        start = time.time()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        duration = round(time.time() - start, 2)
        print(f"✅ OpenAI responded in {duration}s")

        bot_reply = response['choices'][0]['message']['content']
        print("BOT REPLY:", bot_reply)

        # Final checkpoint
        response_data = {"reply": bot_reply}
        print("FINAL RESPONSE DATA:", response_data)

        return jsonify(response_data)

    except Exception as e:
        print("🔥 UNEXPECTED ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
