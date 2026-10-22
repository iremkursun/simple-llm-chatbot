# 🤖 Simple LLM Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2-EE4C2C?logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Transformers-4.41-FFD21E)
![Model](https://img.shields.io/badge/Model-Qwen2.5--0.5B--Instruct-6E44FF)

A lightweight command-line chatbot that runs an open-source, instruction-tuned large language model
**entirely locally on CPU** — no API keys, no cloud services.

Built with Python and Hugging Face Transformers using **Qwen2.5-0.5B-Instruct**.

---

## ✨ Features

- **Assistant-style answers** using the model's native chat template and a configurable system prompt
- **Fact grounding** — verified facts are injected into the system prompt to reduce hallucinations
  (a simple form of Retrieval-Augmented Generation)
- **Conversation memory** — remembers the most recent exchanges for context-aware replies
- **Streaming output** — responses appear token by token, like ChatGPT
- **Multilingual** — replies in the user's language (tested in English and Turkish)
- **Deterministic decoding** — greedy generation with repetition penalty for consistent answers
- **Simple commands** — `/reset` to clear the conversation, `exit` to quit

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

### Run

```bash
python3 chatbot.py
```

The model is downloaded automatically from Hugging Face on the first run.

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

All settings are at the top of `chatbot.py`:

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `Qwen/Qwen2.5-0.5B-Instruct` | Any Hugging Face chat model (e.g. `Qwen/Qwen2.5-1.5B-Instruct`) |
| `SYSTEM_PROMPT` | Helpful assistant + verified facts | Controls the bot's personality, rules and known facts |
| `MAX_HISTORY_TURNS` | `5` | Number of past exchanges kept in memory |
| `MAX_NEW_TOKENS` | `512` | Maximum length of each response |

---

## 🧠 How It Works

1. The user's message is added to the conversation history.
2. The system prompt and the most recent messages are formatted with the model's **chat template**.
3. The model generates a reply with greedy decoding, streaming each token to the terminal.
4. The reply is saved to the history so the next answer has context.

---

## ⚠️ Limitations

Small models (0.5B parameters) have limited world knowledge and can **hallucinate facts**.
Before fact grounding was added, the bot confidently answered:

> *"ChatGPT was developed by Anthropic, an AI research company founded by Elon Musk."*

This is wrong on both counts. Adding verified facts to the system prompt fixed this answer, but
facts outside that list may still be inaccurate. Larger models such as `Qwen2.5-1.5B-Instruct`
or `Qwen2.5-7B-Instruct` are more accurate but need more RAM or a GPU.

---

## 🗺️ Roadmap

- [ ] Load facts from an external file or document (full RAG pipeline)
- [ ] Web interface with Gradio or Streamlit
- [ ] Optional API backend for higher-quality answers
- [ ] Save and load conversation history

---

## 📚 Background

This project started as the IBM Skills Network lab
*"Create Simple Chatbot with Open Source LLMs using Python and Hugging Face"*,
which used `facebook/blenderbot-400M-distill`. It was then upgraded to an
instruction-tuned LLM with a chat template, system prompt, fact grounding and streaming output.

## 🙏 Acknowledgments

- [Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) by Alibaba Cloud
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- IBM Skills Network
