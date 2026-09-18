from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
LLAMA_URL = "http://127.0.0.1:8081/v1/chat/completions"
SYSTEM_PROMPT = (
    "You are MB AI, a helpful concise local AI running on a Raspberry Pi. "
    "Answer clearly and do not claim internet access unless it is actually available."
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
        r = requests.post(
            LLAMA_URL,
            json={
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *safe_messages],
                "temperature": float(data.get("temperature", 0.7)),
                "max_tokens": int(data.get("max_tokens", 256)),
                "stream": False,
            },
            timeout=180,
        )
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except requests.RequestException as e:
        return jsonify({"error": f"Local AI server error: {e}"}), 502
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid model response: {e}"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
