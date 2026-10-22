"""
Simple chatbot using an open-source instruction-tuned LLM (Qwen2.5) with Hugging Face Transformers.
Commands: 'exit' to quit, '/reset' to clear the conversation.
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

# --- Settings ---
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"   # More accurate (needs ~6 GB RAM): "Qwen/Qwen2.5-1.5B-Instruct"
SYSTEM_PROMPT = (
    "You are a helpful, friendly and knowledgeable assistant. "
    "Give clear, accurate and well-structured answers. "
    "If you are not sure about a fact (names, dates, companies, numbers), "
    "say that you are not sure instead of guessing. "
    "Always reply in the same language the user writes in.\n\n"
    "Use these verified facts when relevant:\n"
    "- ChatGPT was developed by OpenAI and released in November 2022.\n"
    "- Claude was developed by Anthropic, founded in 2021 by Dario and Daniela Amodei.\n"
    "- LLaMA is an open-weight model family developed by Meta.\n"
    "- Qwen is an open-weight model family developed by Alibaba Cloud. You are running on Qwen2.5."
)
MAX_HISTORY_TURNS = 5      # how many past user/assistant exchanges to remember
MAX_NEW_TOKENS = 512


def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.bfloat16
    print(f"Loading {MODEL_NAME} on {device}... (first run downloads the model)")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=dtype).to(device)
    model.eval()
    return tokenizer, model, device


def generate_reply(tokenizer, model, device, history):
    # System prompt + only the most recent messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-MAX_HISTORY_TURNS * 2:]

    input_ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(device)

    # Prints tokens as they are generated (ChatGPT-style streaming)
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=torch.ones_like(input_ids),
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            repetition_penalty=1.1,
            streamer=streamer,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Keep only the newly generated part
    return tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True).strip()


def main():
    tokenizer, model, device = load_model()
    history = []
    print("\nChatbot ready! Type 'exit' to quit, '/reset' to start a new conversation.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.lower() == "/reset":
            history = []
            print("Conversation cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})
        print("Bot: ", end="", flush=True)
        reply = generate_reply(tokenizer, model, device, history)
        history.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    main()