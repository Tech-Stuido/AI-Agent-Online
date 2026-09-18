# MB AI Architecture

```text
Browser
  ↓ HTTP
Flask :8080
  ↓ localhost HTTP
llama-server :8081
  ↓
Qwen2.5 0.5B Instruct Q4_K_M
```

Flask owns the website and browser-facing API. llama-server owns inference and is bound to `127.0.0.1`.

## Runtime
- Context: 1024
- Parallel slots: 1
- CPU threads: 4
- Batch: 128
- GPU layers: 0
- Flask: 0.0.0.0:8080
- llama-server: 127.0.0.1:8081

## Storage
Model path:
```text
~/MB-AI/models/qwen2.5-0.5b-instruct-q4_k_m.gguf
```
The GGUF is not committed to GitHub.

## Design goal
Keep the AI small enough for the Raspberry Pi while making the website feel like a complete AI companion without a large frontend framework or cloud inference dependency.
