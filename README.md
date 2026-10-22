cat > /home/project/README.md << 'EOF'
# Simple LLM Chatbot

A command-line chatbot built with Python and Hugging Face Transformers, running the
open-source instruction-tuned model **Qwen2.5-0.5B-Instruct** locally on CPU.

## Features
- Chat template + system prompt for assistant-style answers
- **Verified facts in the system prompt** to reduce hallucinations (a simple form of grounding / RAG)
- Remembers recent conversation context
- Streams responses token by token
- `/reset` to start a new conversation, `exit` to quit
- Replies in the user's language (tested in English and Turkish)

## Setup
```bash
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
python3 chatbot.py