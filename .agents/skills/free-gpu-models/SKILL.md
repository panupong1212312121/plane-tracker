---
name: free-gpu-models
description: Provision a free-tier cloud GPU (Kaggle Notebooks ~P100/T4x2, Google Colab ~T4) and run local open-weight models on it — Ollama/llama.cpp/vLLM — exposed for use from the local machine (ngrok/cloudflared tunnel or direct API in the notebook). Use when the user asks to run a model on free GPU, "ใช้ GPU ฟรี", "โหลดโมเดลบน Kaggle/Colab", "run llama/ollama without a GPU", or wants local-model inference without paying.
---

# Free GPU Models

Run an open-weight model on someone else's free GPU and use it from here. Two platforms, same lifecycle: **provision → set up runtime → expose → consume → tear down**.

## Platform choice

| | Kaggle | Colab |
| --- | --- | --- |
| GPU | P100 16GB or T4 ×2 (15GB) | T4 15GB (free tier) |
| Session | ~9h–12h/week quota, ~30GB disk, `/kaggle/working` persists after shutdown | Quota varies; disk resets per session |
| Best for | Long jobs, 2-GPU inference, DPO/SFT experiments | Quick chats, small serving windows |

Both: interactive login required (user does it in the browser), no secrets committed, GPU is **not guaranteed** on free tier — check availability first and state it.

## Workflow

1. **Pre-flight.** Confirm with the user: target model (fits 15GB? 7B q4 ≈ 4–5GB, 13B q4 ≈ 8–10GB — 70B needs quantization + offloading and often won't fit), platform, and what consumes the model (notebook cells, local scripts via tunnel, or an app).
2. **Notebook scaffolding.** Generate a cell-by-cell notebook the user pastes in: GPU check (`!nvidia-smi`), runtime install, model pull (Ollama install or `llama-cpp-python`/`transformers` with the exact HF repo id), and — if the user wants to call it from their machine — a tunnel cell (ngrok with token from an env var, or cloudflared quick tunnel which needs no token).
3. **Expose safely.** Tunnels are public URLs: bind the model server to a token or path check by default, and say plainly that free-tier tunnels are not production security. Never put the ngrok token or HF token in the notebook output.
4. **Consume.** Give the local call: OpenAI-compatible base URL (e.g. `http://localhost:11434/v1` via a tunnel), one `curl` example, and timeout guidance (cold start on first request is minutes, not seconds).
5. **Teardown.** State the free-tier reality: idle sessions get reclaimed and data outside the persistent directory is lost — anything to keep (LoRA weights, configs, generated data) must be saved to the persistent path, pushed to a hub, or downloaded before shutdown. End with a one-command shutdown/stop cell.

## Guardrails

- Free tiers change limits without notice: verify current quota/limits with web search if the user hits an error, don't quote stale numbers from memory.
- Never claim GPU is available when the quota is exhausted — report the error verbatim and suggest the other platform.
- No paid tier, no credit card, no paid APIs — that's a different conversation; refuse and say why if a step would enable billing.
- Model licensing: note non-commercial licenses (e.g. Llama community) when the model's license restricts use.
- This skill provisions and runs; it does not fine-tune. Training on free tier is a bounded separate task — check disk/time budget honestly before promising it.
