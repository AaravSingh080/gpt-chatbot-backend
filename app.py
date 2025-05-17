@app.route('/chat', methods=['POST'])
def chat():
    try:
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Raw data:", request.data)
        print("Is JSON:", request.is_json)

        data = request.get_json(force=True)
        print("DATA RECEIVED (parsed):", data)

        user_message = data.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
