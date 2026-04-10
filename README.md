CerebroShell 🧠
A GPU-accelerated, AI-augmented terminal with offline natural language command assistance powered by Qwen2.5-7B.

What is CerebroShell?
Traditional terminals are powerful but unforgiving — strict syntax, no guidance, and zero tolerance for typos. CerebroShell adds an intelligent AI layer between you and the shell, letting you type natural language when you need it and raw commands when you don't. Everything runs completely offline. No cloud, no privacy trade-offs, no latency surprises.
Under the hood, it's three layers:
┌─────────────────────────────┐
│       Terminal (OpenGL)     │  ← GPU-accelerated rendering
├─────────────────────────────┤
│       AI Layer (Qwen2.5-7B) │  ← Natural language → shell command
├─────────────────────────────┤
│       Bash (Execution)      │  ← Actual command execution
└─────────────────────────────┘

How It Works
CerebroShell has two modes, toggled by how you submit input:
Normal Mode — Enter
Type a shell command and press Enter. It executes directly through Bash. No AI involved, no overhead.
user > ls -la
(output)
AI Mode — Shift+Enter
Type a natural language query and press Shift+Enter. The query goes to Qwen2.5-7B locally, which suggests the equivalent shell command. You confirm before anything runs.
user > create a new folder named projects    [Shift+Enter]

Suggested Command: mkdir projects
Run this command? (y/n): y

Running command...
If you press n, nothing executes and you're back at the prompt. You stay in control at all times.

Demo
Python Prototype — AI-assisted command execution
<img width="1474" height="751" alt="img1" src="https://github.com/user-attachments/assets/d5f720cc-d5da-4a2e-a832-108099822251" />

Python Prototype — Natural language to shell command
<img width="801" height="635" alt="img2" src="https://github.com/user-attachments/assets/e04052b6-7d45-4d64-8b65-4ff983d08baa" />

Tech Stack
ComponentTechnologyTerminal renderingOpenGL 3.3 (GPU-accelerated)AI layerQwen2.5-7B (offline, via Ollama / llama.cpp)Execution layerBashCore implementationC++, Python

Requirements

OS: Linux, macOS, or Windows
OpenGL 3.3+
Python 3.10+
RAM: ≥ 16 GB recommended
GPU: ≥ 4 GB VRAM recommended (CPU with AVX2 also works)
Ollama or llama.cpp for local LLM inference


Installation
bashgit clone https://github.com/rdmis07/CerebroShell.git
cd CerebroShell
# setup instructions here

Author
Rudransh Mishra
