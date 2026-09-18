from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
LLAMA_URL = "http://127.0.0.1:8081/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are MB AI, a helpful concise local AI running on a Raspberry Pi. "
    "Answer the user's request directly and be useful. "
    "Do not start with generic phrases like 'Sorry, I can't help with that' when you can provide a useful answer. "
    "If a request is unclear, ask a short clarifying question or make a reasonable assumption. "
    "If a request is unsafe or you genuinely cannot comply, briefly explain the limitation and offer a safe alternative. "
    "For normal questions, do not refuse unnecessarily. "
    "Do not claim internet access unless it is actually available."
)

REFUSAL_RETRY_PROMPT = (
    "Answer the user's request directly and helpfully. "
    "Do not give a generic refusal. "
    "If the request cannot be fulfilled, explain the specific limitation and provide the closest safe, useful alternative. "
    "Keep the answer concise."
)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        r = requests.get("http://127.0.0.1:8081/health", timeout=3)
        return jsonify({"ok": r.ok, "llama": r.ok})
    except requests.RequestException:
        return jsonify({"ok": False, "llama": False}), 503


def ask_llama(messages, temperature, max_tokens):
    r = requests.post(
        LLAMA_URL,
        json={
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        },
        timeout=180,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def looks_like_generic_refusal(reply):
    text = reply.lower()
    refusal_phrases = (
        "sorry, i can't help",
        "sorry, i cannot help",
        "i can't help with that",
        "i cannot help with that",
        "i'm sorry, i can't",
        "i'm sorry, i cannot",
    )
    return any(phrase in text for phrase in refusal_phrases)


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    incoming = data.get("messages", [])

    if not isinstance(incoming, list):
        return jsonify({"error": "messages must be a list"}), 400

    safe_messages = []
    for item in incoming[-12:]:
        if isinstance(item, dict) and item.get("role") in {"user", "assistant"}:
            content = str(item.get("content", ""))[:8000]
            if content:
                safe_messages.append({"role": item["role"], "content": content})

    try:
        temperature = float(data.get("temperature", 0.7))
        max_tokens = int(data.get("max_tokens", 256))

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *safe_messages,
        ]
        reply = ask_llama(messages, temperature, max_tokens)

        # Tiny local models can sometimes produce a canned refusal even for
        # ordinary questions. Give the model one additional instruction pass.
        if looks_like_generic_refusal(reply) and safe_messages:
            retry_messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *safe_messages,
                {"role": "assistant", "content": reply},
                {"role": "user", "content": REFUSAL_RETRY_PROMPT},
            ]
            retry = ask_llama(retry_messages, temperature, max_tokens)
            if retry:
                reply = retry

        return jsonify({"reply": reply})

    except requests.RequestException as e:
        return jsonify({"error": f"Local AI server error: {e}"}), 502
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid model response: {e}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
