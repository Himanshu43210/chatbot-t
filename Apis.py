from flask import Flask, jsonify, request
import sys
from flask_cors import CORS  # Import CORS

# Assuming the function chat_with_user is in a file named chat.py
sys.path.append("./products/BuilderfloorChatbot")
from chatbot import text_to_text_conversation

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# If you need to set specific CORS options, you can do so:
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(
        force=True
    )  # Ensure we get JSON even if the content-type header is not set.

    userQuestion = data.get("userQuestion", "")
    history = data.get("history", "")
    openai_key = data.get("openai_key", "")  # Extract OpenAI key from request JSON
    print("Form Apis: ", openai_key)
    # Pass the OpenAI key to the chatbot
    response = text_to_text_conversation(
        userQuestion,
        history,
        "products/BuilderfloorChatbot/builder_floor.csv",
        openai_key,
    )

    return jsonify({"data": response}), 200


if __name__ == "__main__":
    app.run(debug=True)
