# Free GPU Platform Comparison

Detailed notes on each free/cheap platform for fine-tuning.

---

## Google Colab

| Tier | GPU | VRAM | RAM | Disk | Session Limit |
|------|-----|------|-----|------|---------------|
| Free | T4 | 16GB | 12GB | 78GB | ~2h runtime |
| Pay-As-You-Go | T4/L4/A100 | 16-80GB | 25-52GB | 166GB | 24h+ (100 compute units) |
| Pro | T4/V100/A100 | 16-40GB | 25-52GB | 166GB | ~24h |

**Free Tier Constraints:**
- Runtime disconnects after ~90 min of inactivity or ~2h total
- No guaranteed GPU allocation — sometimes CPU-only
- Session state lost on disconnect (save to Google Drive or Hugging Face)

**Tips:**
- Mount Google Drive to persist datasets and checkpoints
- Use `!pip install` in notebook cells (persists for session only)
- Save checkpoints to HF Hub mid-training: `model.push_to_hub("my-model")`
- Use `wandb` offline mode + sync later

---

## Kaggle Notebooks

| Feature | Detail |
|---------|--------|
| GPU | T4 x2 or P100 (varies) |
| VRAM | 16GB per GPU |
| Session Limit | 30h/week GPU |
| Internet | Disabled by default (can enable) |
| Dataset Limit | 20GB per dataset |

**Pros:**
- Can use 2 GPUs (DP/DataParallel) for larger batches
- 30h/week is generous
- Built-in datasets API

**Cons:**
- No internet unless explicitly enabled
- Week cap resets Sunday UTC
- 9h max session runtime

---

## Lightning AI (lightning.ai)

| Feature | Detail |
|---------|--------|
| GPU | T4, A10G |
| VRAM | 16-24GB |
| Session Limit | 8h (free tier) |
| Storage | Persistent (survives sessions) |

**Pros:**
- Persistent storage — your files stay between sessions
- Studio environment (VS Code-like)
- Multi-GPU available

**Cons:**
- Limited free tier ($10 credit/month, then pay)
- Fewer community notebooks than Colab

---

## Hugging Face Spaces (ZeroGPU)

| Feature | Detail |
|---------|--------|
| GPU | T4 |
| VRAM | 16GB |
| Queue | Shared — wait for GPU |
| Persistence | Yes (Space filesystem) |

**Pros:**
- Free, persistent
- Tight HF Hub integration
- Gradio interface possible

**Cons:**
- Queue waiting on busy days
- No guarantees on availability
- Shared GPU (queue-based)

---

## Modal

| Feature | Detail |
|---------|--------|
| GPU | A10G, A100 |
| VRAM | 24GB+ |
| Credits | $20/mo free signup |
| Model | Pay-per-second serverless |

**Pros:**
- Serious compute (A100 available)
- Serverless — no notebook UI needed
- Python SDK, great for production pipelines

**Cons:**
- Not notebook-based (script-driven)
- Free credits run out fast with A100
- Requires SDK setup

---

## Summary Decision Matrix

| Your Goal | Best Platform |
|-----------|---------------|
| Quick experiment, small model (<3B) | Colab Free |
| Medium model (7B) LoRA | Colab Free / Kaggle |
| Large model (13-70B) QLoRA | Colab Pay-As-You-Go / Lightning |
| Preference alignment (DPO/GRPO) | Kaggle (2 GPUs) / Modal |
| Production pipeline | Modal / HF Spaces |
| No GPU, just API calls | Together / DeepSeek API |
| Web UI, non-technical | LLaMA-Factory on HF Spaces |
