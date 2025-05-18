from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print("USER:", user_message)

        start = time.time()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content.strip()
        duration = round(time.time() - start, 2)
        print(f"BOT REPLY ({duration}s):", bot_reply)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
