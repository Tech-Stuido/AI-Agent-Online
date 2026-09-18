# MB AI — Local Raspberry Pi AI Assistant

MB AI is a lightweight local AI assistant built for a Raspberry Pi 4. The website is designed as the main user interface while keeping model inference local.

## Core stack
- Raspberry Pi 4 Model B
- Debian GNU/Linux 13 (trixie), arm64
- Python 3, Flask, Requests
- llama.cpp / llama-server
- Qwen2.5 0.5B Instruct Q4_K_M GGUF
- HTML/CSS/JavaScript
- Browser localStorage for chat history

## Local-only architecture
**No API key is used by the core chat path. No cloud AI model is required.**

```text
Browser → Flask :8080 → llama-server :8081 → Qwen2.5 0.5B
```

Flask is the browser-facing server. llama-server stays on `127.0.0.1:8081`, so the model endpoint is not directly exposed to the LAN.

## Website version
The website now includes:
- MB AI branded responsive UI
- rounded-square animated AI face
- expressive eyes and mouth
- idle, listening, thinking, talking and surprised states
- multiple browser chats
- new-chat and clear-chat controls
- localStorage chat saving
- quick prompts
- Enter/Shift+Enter controls
- typing animation
- local model health indicator
- dark, midnight and light themes
- optional browser text-to-speech
- browser SpeechRecognition input when supported
- mobile/touch layout
- settings panel

Browser speech features depend on browser/OS support. Fully offline STT/TTS remains a separate backend milestone.

## Project layout
```text
AI-Agent-Online/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/index.html
├── static/style.css
├── static/app.js
└── docs/
    ├── ARCHITECTURE.md
    ├── COMMANDS.md
    └── WEB_FEATURES.md
```

## Raspberry Pi commands used

### Check the system
```bash
cat /etc/os-release
uname -m
df -h
free -h
```

### Create the project
```bash
mkdir -p ~/MB-AI/models
cd ~/MB-AI
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Build llama.cpp
```bash
cd ~
git clone https://github.com/ggerganov/llama.cpp.git
cd ~/llama.cpp
cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_TESTS=OFF
cmake --build build -j2
```

### Model path
```text
~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf
```

The GGUF is intentionally excluded from GitHub.

### Start llama-server
```bash
~/llama.cpp/build/bin/llama-server \
  -m ~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  -c 1024 -np 1 -t 4 -b 128 -ngl 0 \
  --host 127.0.0.1 --port 8081
```

### Start the website
Open a second terminal:
```bash
cd ~/MB-AI
./venv/bin/python app.py
```

Open:
```text
http://127.0.0.1:8080
http://<PI-LAN-IP>:8080
```

Previous working LAN example: `http://192.168.1.180:8080`.

### Health/debug commands
```bash
ss -ltnp | grep 8080
ss -ltnp | grep 8081
curl http://127.0.0.1:8081/health
curl http://127.0.0.1:8080
ps aux | grep -E 'app.py|llama-server'
```

Stop each foreground server with `Ctrl+C`.

## Current performance settings
- Qwen2.5 0.5B
- Q4_K_M quantization
- context 1024
- one parallel slot
- 4 CPU threads
- batch 128
- 0 GPU layers

These settings are intentionally small for the Raspberry Pi's memory limits.

## Roadmap
1. Token streaming
2. Markdown and code rendering
3. Copy/regenerate controls
4. Better persistent chat database
5. PWA install/offline shell
6. Fully offline STT
7. Fully offline TTS
8. Optional Pi camera vision
9. Separate permissioned robot-control tools
10. Live AI-face state synchronization

See `docs/COMMANDS.md`, `docs/WEB_FEATURES.md`, and `docs/ARCHITECTURE.md`.
