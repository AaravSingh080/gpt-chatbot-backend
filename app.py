from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from anywhere (frontend, Hoppscotch, etc.)

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define chat route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Debug logs to track what's being received
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Raw data:", request.data)
        print("Is JSON:", request.is_json)

        # Force Flask to treat it as JSON
        data = request.get_json(force=True)
        print("DATA RECEIVED (parsed):", data)

        user_message = data.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Call OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        # Extract reply
        bot_reply = response['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# Start Flask app on Render
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
