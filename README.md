# 🤖 Simple LLM Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2-EE4C2C?logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Transformers-4.41-FFD21E)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)
![Model](https://img.shields.io/badge/Model-Qwen2.5--0.5B--Instruct-6E44FF)

A lightweight chatbot that runs an open-source, instruction-tuned large language model
**entirely locally on CPU** — no API keys, no cloud services.

Use it from the **terminal** or through a **web interface** powered by a Flask backend.

---

## ✨ Features

- **Web chat interface** — Flask backend with a `/chatbot` REST endpoint and an HTML/JS frontend
- **Command-line mode** — chat directly in the terminal with streaming output
- **Assistant-style answers** using the model's native chat template and a configurable system prompt
- **Fact grounding** — verified facts are injected into the system prompt to reduce hallucinations
  (a simple form of Retrieval-Augmented Generation)
- **Conversation memory** — remembers the most recent exchanges for context-aware replies
- **Multilingual** — replies in the user's language (tested in English and Turkish)
- **Deterministic decoding** — greedy generation with repetition penalty for consistent answers

---

## 📁 Project Structure

```
simple-llm-chatbot/
├── app.py              # Flask server: serves the web UI and the /chatbot API
├── chatbot.py          # Model loading, prompt building and generation (+ CLI mode)
├── requirements.txt
├── static/             # Frontend JavaScript, CSS and images
└── templates/
    └── index.html      # Chat web page
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or later
- ~2 GB of free RAM and ~1 GB of disk space for the model

### Installation

```bash
git clone https://github.com/iremkursun/simple-llm-chatbot.git
cd simple-llm-chatbot

python3 -m venv my_env
source my_env/bin/activate        # Windows: my_env\Scripts\activate

pip install -r requirements.txt
```

The model is downloaded automatically from Hugging Face on the first run.

### Option 1 — Web interface

```bash
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### Option 2 — Terminal

```bash
python3 chatbot.py
```

Type `/reset` to start a new conversation and `exit` to quit.

---

## 🔌 API

The backend exposes a single endpoint:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"prompt": "Who developed ChatGPT?"}' \
     http://127.0.0.1:5000/chatbot
```

Response (plain text):

```
ChatGPT was developed by OpenAI.
```

---

## 💬 Example

```
You: Who developed ChatGPT?
Bot: ChatGPT was developed by OpenAI.

You: What is my favorite color?
Bot: As an AI language model, I don't have personal preferences or emotions like humans do.
     However, I can provide information about different colors if you're interested!

You: Python'da bir listeyi nasıl ters çeviririm?
Bot: 1. reverse() metodunu kullanabilirsiniz:
        lst.reverse()
     2. Slicing ile:
        reversed_list = lst[::-1]
```

---

## ⚙️ Configuration

All model settings are at the top of `chatbot.py`:

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `Qwen/Qwen2.5-0.5B-Instruct` | Any Hugging Face chat model (e.g. `Qwen/Qwen2.5-1.5B-Instruct`) |
| `SYSTEM_PROMPT` | Helpful assistant + verified facts | Controls the bot's personality, rules and known facts |
| `MAX_HISTORY_TURNS` | `5` | Number of past exchanges kept in memory |
| `MAX_NEW_TOKENS` | `512` | Maximum length of each response |

---

## 🧠 How It Works

1. The browser sends the user's message to `POST /chatbot` as JSON: `{"prompt": "..."}`.
2. Flask adds the message to the conversation history.
3. The system prompt and the most recent messages are formatted with the model's **chat template**.
4. Qwen2.5 generates a reply with greedy decoding.
5. The reply is saved to the history and returned to the browser, which shows it in a chat bubble.

`app.py` reuses `load_model()` and `generate_reply()` from `chatbot.py`, so the web and terminal
versions share exactly the same model logic.

---

## ⚠️ Limitations

Small models (0.5B parameters) have limited world knowledge and can **hallucinate facts**.
Before fact grounding was added, the bot confidently answered:

> *"ChatGPT was developed by Anthropic, an AI research company founded by Elon Musk."*

This is wrong on both counts. Adding verified facts to the system prompt fixed this answer, but
facts outside that list may still be inaccurate. Larger models such as `Qwen2.5-1.5B-Instruct`
or `Qwen2.5-7B-Instruct` are more accurate but need more RAM or a GPU.

The web server keeps a single shared conversation history, so it is intended for one user at a time.

---

## 🗺️ Roadmap

- [x] Command-line chatbot with an instruction-tuned LLM
- [x] Flask backend and web chat interface
- [ ] Per-user conversation sessions
- [ ] Load facts from an external file or document (full RAG pipeline)
- [ ] Stream responses to the web interface
- [ ] Optional API backend for higher-quality answers

---

## 📚 Background

This project was built while completing two IBM Skills Network labs:

1. *Create Simple Chatbot with Open Source LLMs using Python and Hugging Face*
2. *Integrating your Chatbot into a Web Interface*

The labs used `facebook/blenderbot-400M-distill`. This version upgrades it to an instruction-tuned
LLM with a chat template, system prompt, fact grounding and a shared model module for both the
web and terminal versions.

![Chatbot web interface](screenshot.png)

## 🙏 Acknowledgments

- [Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) by Alibaba Cloud
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- Web interface template from
  [IBM Skills Network — LLM_application_chatbot](https://github.com/ibm-developer-skills-network/LLM_application_chatbot)
