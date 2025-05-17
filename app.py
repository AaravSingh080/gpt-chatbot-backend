from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Create OpenAI client (v1.0+)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if request.content_length == 0:
            return jsonify({"error": "Empty request body"}), 400

        data = request.get_json(force=True)
        user_message = data.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        start = time.time()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        duration = round(time.time() - start, 2)
        bot_reply = response.choices[0].message.content
        print(f"✅ OpenAI replied in {duration}s → {bot_reply}")
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
