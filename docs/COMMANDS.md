# MB AI Command History

## System checks
```bash
cat /etc/os-release
uname -m
df -h
free -h
```

Working environment: Raspberry Pi 4, Debian GNU/Linux 13 (trixie), arm64.

## Project setup
```bash
mkdir -p ~/MB-AI/models
cd ~/MB-AI
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## llama.cpp
```bash
cd ~
git clone https://github.com/ggerganov/llama.cpp.git
cd ~/llama.cpp
cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_TESTS=OFF
cmake --build build -j2
```

## Model
Expected local file:
```text
~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf
```

It is excluded from GitHub with `*.gguf`.

## Start llama-server
```bash
~/llama.cpp/build/bin/llama-server \
  -m ~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  -c 1024 -np 1 -t 4 -b 128 -ngl 0 \
  --host 127.0.0.1 --port 8081
```

## Start the website
Use a second terminal:
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

## Diagnostics
```bash
ss -ltnp | grep 8080
ss -ltnp | grep 8081
curl http://127.0.0.1:8081/health
curl http://127.0.0.1:8080
ps aux | grep -E 'app.py|llama-server'
```

Stop foreground servers with `Ctrl+C`.

## Architecture
```text
Browser → Flask :8080 → llama-server :8081 → Qwen2.5 0.5B
```
