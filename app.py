from flask import Flask, request, render_template
from flask_cors import CORS

from chatbot import load_model, generate_reply   # reuse the Qwen chatbot from lab 1

app = Flask(__name__)
CORS(app)

# Load the model once when the server starts
tokenizer, model, device = load_model()
conversation_history = []


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    # Read prompt from HTTP request body
    data = request.get_json()
    input_text = data["prompt"]

    # Generate the response (system prompt + recent history are handled in chatbot.py)
    conversation_history.append({"role": "user", "content": input_text})
    response = generate_reply(tokenizer, model, device, conversation_history)
    conversation_history.append({"role": "assistant", "content": response})

    return response


if __name__ == '__main__':
    app.run()
