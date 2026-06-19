# 🧠 Finetune Lab

> Fine-tuning LLMs on Google Colab (and free alternatives) — notebooks, research, and notes.

A living collection of fine-tuning recipes, experiments, and findings using free/cheap GPU compute (Colab, Kaggle, Lightning AI, Hugging Face Spaces, etc.). No paid GPUs required — everything runs under free tier limits.

---

## 🎯 What This Is

- Ready-to-run **Jupyter notebooks** for LoRA, QLoRA, full fine-tuning, and preference alignment (DPO/GRPO)
- **Research & benchmarks** comparing techniques, hyperparameters, and platform performance
- **Scripts & configs** to reproduce the exact training setups
- A personal lab for documenting what works (and what doesn't) on limited compute

---

## 📁 Structure

```
finetune-lab/
├── notebooks/              # Jupyter notebooks — drop into Colab & run
│   ├── lora/              # LoRA / QLoRA fine-tuning
│   ├── full/              # Full parameter fine-tuning
│   ├── pref/              # Preference alignment (DPO, GRPO, ORPO)
│   └── setup/             # Colab remote connection notebooks
│       ├── colab-server-tunnel.ipynb   # Jupyter + Cloudflare tunnel
│       └── colab-server-vscode.ipynb   # VS Code Remote Tunnel
├── research/              # Findings, technique analysis, comparisons
│   ├── techniques.md      # Deep dives into fine-tuning methods
│   ├── platforms.md       # Free GPU platform comparisons
│   └── colab-connect.md   # 📘 Full guide: remote Colab access methods
├── scripts/               # Utility scripts
│   └── colab-client.py    # CLI client for remote Jupyter API calls
├── data/                  # Dataset notes, preprocessing, preparation
│   └── datasets.md        # Dataset catalogue & prep workflows
├── configs/               # YAML/JSON hyperparameter templates
│   └── hyperparameters/   # Per-model configs (llama, mistral, qwen, etc.)
└── cache/                 # Local cache for models/datasets (gitignored)
```

---

## Agentic Datasets

Research-backed catalog of the **best public datasets for training agentic LLMs**
— tool calling, multi-step reasoning, agent traces, and function calling.

| Tier | Focus | Top Datasets |
|------|-------|-------------|
| ★ — Agent Traces | Reasoning + tool use | `lambda/hermes-agent-reasoning-traces`, `DJLougen/hermes-agent-traces-filtered` |
| ★★ — Function Calling | Tool dispatch accuracy | `glaiveai/glaive-function-calling-v2`, `NousResearch/hermes-function-calling-v1` |
| ★★★ — Agent Instruction | Reasoning depth | `microsoft/orca-agentinstruct-1M-v1`, `zai-org/AgentInstruct` |

The QLoRA notebook uses a **customisable dataset mix** — edit the `DATASET_MIX`
array to change ratios, add/remove sources.

→ Full catalog at [`data/datasets.md`](data/datasets.md)

## Remote Colab Access

One-click method to connect your local machine to a Colab runtime for
interactive development while training runs.

**Quick Open** — click any notebook to launch it in Colab immediately:

| Notebook | Colab Link |
|----------|------------|
| QLoRA Fine-Tuning (Qwen2.5-7B) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/lora/example_qlora_colab.ipynb) |
| DPO Alignment | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/pref/example_dpo_colab.ipynb) |
| Jupyter Lab Tunnel (Cloudflare) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/setup/colab-server-tunnel.ipynb) |
| VS Code Remote Tunnel | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/setup/colab-server-vscode.ipynb) |

**The workflow:**
1. Click a badge → Colab opens the notebook live from GitHub
2. Set runtime to **T4 GPU** (Runtime → Change runtime type → T4)
3. Run all cells — deps install automatically
4. Save results to Drive / push back to GitHub

📘 Full comparison of all methods → [`research/colab-connect.md`](research/colab-connect.md)

---

## 🚀 Quick Start

1. **Pick a notebook** from `notebooks/` that matches your goal
2. **Open in Google Colab** (File → Upload Notebook, or open from GitHub)
3. **Set your runtime** to a T4 GPU (Runtime → Change runtime type → T4)
4. **Run all cells** — dependencies install automatically in Colab

**Example:**

```bash
# Clone the repo locally for reference
git clone https://github.com/ghassan-gaidi/finetune-lab.git
```

Or just browse & click on GitHub — Colab opens notebooks directly via:
`https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/...`

---

## 🧪 Techniques Covered

| Technique | Memory | Speed | Quality | Best For |
|-----------|--------|-------|---------|----------|
| **QLoRA** (4-bit) | Very Low | Fast | Good | Most tasks on free GPUs |
| **LoRA** (16-bit) | Low | Fast | Good | When you can fit the base model |
| **Full Fine-tune** | High | Slow | Best | Domain adaptation, large data |
| **DPO / GRPO** | Low-Moderate | Moderate | Very Good | Alignment, instruction tuning |
| **Unsloth** | Very Low | 2x Faster | Identical | Optimized LoRA/QLoRA on Colab |

---

## 🖥️ Free GPU Platform Comparison

| Platform | GPU | VRAM | Runtime Limit | Pros | Cons |
|----------|-----|------|---------------|------|------|
| **Google Colab (Free)** | T4 | 16GB | ~2h continuous | Easy, pre-installed libs | Timeout, no persistence |
| **Google Colab (Pay-As-You-Go)** | T4/L4/A100 | 16-80GB | 24h+ | More reliable | $10-30/mo |
| **Kaggle Notebooks** | T4 x2 (P100) | 16GB | 30h/week | 2 GPUs, longer sessions | Week cap, no internet |
| **Lightning AI** | T4/A10G | 16-24GB | 8h/session | Persistent storage | Limited free tier |
| **HF Spaces (ZeroGPU)** | T4 | 16GB | Shared queue | Free, persistent | Queue waiting |
| **Modal** | A10G (via free credits) | 24GB | Pay per second | Serverless, scaling | $20 signup credit |
| **RunPod** | Various | Varies | Pay per hour | Cheap spot instances | No meaningful free tier |
| **DeepSeek / Together** | API | — | — | No GPU needed | Costs per token |

> ⚠️ Colab free tier disconnects after ~2h and kills the runtime. Use checkpoints.

---

## 📚 Resources & References

- [Unsloth Documentation](https://github.com/unslothai/unsloth) — Optimized 2x faster LoRA
- [Hugging Face TRL](https://huggingface.co/docs/trl) — SFTTrainer, DPOTrainer, GRPOTrainer
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) — YAML-based fine-tuning framework
- [PEFT](https://huggingface.co/docs/peft) — Parameter-Efficient Fine-Tuning library
- [Bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) — 4/8-bit quantization
- [Llama Factory](https://github.com/hiyouga/LLaMA-Factory) — Web UI for fine-tuning

---

## 📝 License

MIT — feel free to use, adapt, and contribute.

---

**Maintained by [@ghassan-gaidi](https://github.com/ghassan-gaidi)** — experiments in efficient fine-tuning on zero budget.
