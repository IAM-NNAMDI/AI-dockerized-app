from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
from flask import render_template

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Debug check (optional but useful)
print("KEY LOADED:", os.getenv("GROQ_API_KEY") is not None)

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ai', methods=['POST'])
def ai():
    try:
        # Get JSON data from request
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_input = data["message"]

        # Call Groq LLM
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"response": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
