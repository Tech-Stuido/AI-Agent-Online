# MB AI — Website Version

This repository is for the **MB AI website version only**.

MB AI is a local AI web interface designed to run on a Raspberry Pi. The website provides the user interface; the local model is connected through the small Flask backend.

## What is included in the website

- Modern MB AI dashboard
- Responsive desktop and mobile UI
- Rounded-square AI face
- Expressive eyes and mouth
- Idle, listening, thinking, talking, and surprised face states
- Chat messages
- Multiple chats
- New chat
- Clear chat
- Browser chat history with localStorage
- Quick prompt buttons
- Enter to send
- Shift+Enter for a new line
- Typing animation
- Local AI online/offline indicator
- Dark, Midnight, and Light themes
- Settings panel
- Optional browser text-to-speech
- Browser speech-recognition microphone button when supported
- Touch-friendly mobile controls

## Website architecture

```text
Web Browser
    ↓
MB AI Website
    ↓
Flask :8080
    ↓
llama-server :8081
    ↓
Qwen2.5 0.5B Instruct Q4_K_M
```

The website itself does not contain the model. The GGUF model stays on the Raspberry Pi.

## Important

The website's core chat does **not** require an API key and does not require a cloud AI service.

Browser voice recognition varies by browser and operating system. The microphone button is a website feature, but fully offline speech recognition is not guaranteed by the browser API.

---

# Raspberry Pi Installation Instructions

These instructions reproduce the website setup we used.

## 1. Check the Pi

Run:

```bash
cat /etc/os-release
uname -m
df -h
free -h
```

The working machine is a Raspberry Pi 4 using Debian GNU/Linux 13 (trixie), arm64.

## 2. Create the MB AI folder

```bash
mkdir -p ~/MB-AI/models
cd ~/MB-AI
```

## 3. Create the Python environment

```bash
python3 -m venv venv
```

Activate it if desired:

```bash
source venv/bin/activate
```

Install the website requirements:

```./venv/bin/pip install -r requirements.txt
```

## 4. Build llama.cpp

Go to your home directory:

```bash
cd ~
```

Clone llama.cpp:

```bash
git clone https://github.com/ggerganov/llama.cpp.git
```

Build it:

```bash
cd ~/llama.cpp
cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_TESTS=OFF
cmake --build build -j2
```

The server should then exist at:

```text
~/llama.cpp/build/bin/llama-server
```

## 5. Install the model

Place the Qwen2.5 0.5B Instruct Q4_K_M GGUF model here:

```text
~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf
```

The model is intentionally not included in this GitHub repository because GGUF model files are large.

## 6. Start the local AI model

Open Terminal 1:

```bash
~/llama.cpp/build/bin/llama-server \
  -m ~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  -c 1024 \
  -np 1 \
  -t 4 \
  -b 128 \
  -ngl 0 \
  --host 127.0.0.1 \
  --port 8081
```

Leave this terminal running.

## 7. Start the MB AI website

Open Terminal 2:

```bash
cd ~/MB-AI
./venv/bin/python app.py
```

Flask should report port 8080.

Open the website on the Pi:

```text
http://127.0.0.1:8080
```

From another device on the same network:

```text
http://<PI-LAN-IP>:8080
```

The previous working Pi address was:

```text
http://192.168.1.180:8080
```

Use your Pi's current LAN IP if it has changed.

---

# Useful Commands

## Check Flask

```bash
ss -ltnp | grep 8080
```

## Check llama-server

```bash
ss -ltnp | grep 8081
```

## Check the model server

```bash
curl http://127.0.0.1:8081/health
```

## Check the website

```bash
curl http://127.0.0.1:8080
```

## Find running MB AI processes

```bash
ps aux | grep -E 'app.py|llama-server'
```

## Stop the servers

Press:

```text
Ctrl+C
```

in the terminal running the server.

---

# Performance Configuration

The website is intentionally paired with a small local model for the Raspberry Pi.

Current llama-server settings:

```text
Model:       Qwen2.5 0.5B Instruct Q4_K_M
Context:     1024
Slots:       1
CPU threads: 4
Batch:       128
GPU layers:  0
Flask:       0.0.0.0:8080
llama:       127.0.0.1:8081
```

This keeps the model endpoint local and keeps the website lightweight.

---

# Project Structure

```text
AI-Agent-Online/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── docs/
    ├── ARCHITECTURE.md
    ├── COMMANDS.md
    └── WEB_FEATURES.md
```

## Main website files

**app.py**  
Runs the Flask website and connects the browser chat to the local llama-server.

**templates/index.html**  
Contains the MB AI website structure.

**static/style.css**  
Contains the complete website styling and responsive layout.

**static/app.js**  
Controls chat history, face states, voice input, text-to-speech, settings, themes, and the chat API.

**requirements.txt**  
Contains the small Python dependencies required by the website.

---

# Website Development Roadmap

Future website-only improvements can include:

- Streaming AI responses
- Markdown rendering
- Code blocks
- Copy response button
- Regenerate response
- Message editing
- Search chats
- Better chat organization
- PWA installation
- More expressive face animations
- Better voice controls
- Fully offline browser-compatible STT integration
- Fully offline TTS integration
- Camera/vision interface
- Live face animation synchronized with generated text

The focus of this repository is the **MB AI website experience**.
