from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
# Load environment variables from .env file
load_dotenv()

# Assuming the function chat_with_user is in a file named chatbot.py
sys.path.append("./products/BuilderfloorChatbot")
from chatbot import text_to_text_conversation

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the OpenAI key from the .env file
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("No OpenAI API key set in .env file")


@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(force=True)

    userQuestion = data.get("userQuestion", "")
    history = data.get("history", "")

    # No longer necessary to extract OpenAI key from request JSON
    # Use the key loaded from the .env file instead
    response = text_to_text_conversation(
        userQuestion,
        history,
        "products/BuilderfloorChatbot/builder_floor.csv",
        openai_key,
    )

    return jsonify({"data": response}), 200


if __name__ == "__main__":
    app.run(debug=True)
