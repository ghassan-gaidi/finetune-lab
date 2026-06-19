# 🔌 Connecting to Google Colab Remotely

Multiple ways to access a Colab runtime from external tools — browser, VS Code,
or command-line.

---

## Method 1: Cloudflare Tunnel + Jupyter Lab (Browser)

**Best for:** Browser-based notebook editing + the Hermes agent¹ / CLI.

**Notebook:** `notebooks/setup/colab-server-tunnel.ipynb`
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/setup/colab-server-tunnel.ipynb)

Runs Jupyter Lab on the Colab VM and tunnels it through Cloudflare (no auth
required). You get a `*.trycloudflare.com` URL.

**Connect from browser:**
```
{URL}/lab?token=colab-finetune
```

**Connect from terminal (Hermes / CLI):**
```bash
# Set once from the Colab notebook output
export COLAB_URL="https://xxx.trycloudflare.com"

# List files on the Colab VM
python3 scripts/colab-client.py --url $COLAB_URL ls

# Execute code
python3 scripts/colab-client.py --url $COLAB_URL exec "import torch; print(torch.cuda.is_available())"

# Upload + run a notebook
python3 scripts/colab-client.py --url $COLAB_URL run notebooks/lora/example_qlora_colab.ipynb

# Create a new notebook
python3 scripts/colab-client.py --url $COLAB_URL create experiments/new-ft.ipynb
```

**Requires:** `pip install requests websocket-client`

> ¹ The cloudflared URL changes every Colab session. The agent stores it as an
> env var and uses the `scripts/colab-client.py` for execution.

---

## Method 2: VS Code Remote Tunnel

**Best for:** Full IDE — code, debug, terminal, extensions.

**Notebook:** `notebooks/setup/colab-server-vscode.ipynb`
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/setup/colab-server-vscode.ipynb)

Uses VS Code's built-in Remote Tunnel feature. One-time GitHub auth, then you
connect from VS Code Desktop or `vscode.dev`.

```
┌──────────┐     tunnel     ┌─────────────┐
│ VS Code   │◄──────────────│ Colab VM    │
│ Desktop   │               │ (GPU, 12GB) │
└──────────┘               └─────────────┘
```

**Steps:**
1. Open the Colab notebook, run the bootstrap cell (downloads VS Code CLI)
2. Run login — you'll get a device code URL
3. Open the URL, enter the code, authorize with GitHub
4. Run the tunnel cell — it starts `code tunnel --name colab-gpu`
5. On your local machine: VS Code → Remote Explorer → Connect to Tunnel → `colab-gpu`

**No re-login needed** on subsequent Colab sessions if the `--cli-data-dir` persists
(sessions with the same VM usually keep `/content/`).

---

## Method 3: Google Drive Sync

**Best for:** Simple workflow — edit locally, run in Colab, save results.

1. Save notebooks to a Google Drive folder
2. In Colab: `File → Open Notebook → Google Drive` 
3. Mount Drive with:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
4. Save output back to Drive

Not programmatic but zero setup.

---

## Method 4: GitHub ↔ Colab Direct Link

**Best for:** Iterating on notebooks stored in this repo.

Every notebook in this repo has a `[Open In Colab]` badge. You can also link
directly:

```
https://colab.research.google.com/github/ghassan-gaidi/finetune-lab/blob/main/notebooks/lora/example_qlora_colab.ipynb
```

**Workflow:**
1. Edit notebook locally → commit & push to GitHub
2. Open in Colab via the link (always reflects latest version)
3. Run on GPU
4. `File → Save a copy in Drive` to keep results
5. (Optional) Download the executed notebook and commit back

---

## Method 5: Modal (Free GPU, Serverless)

**Best for:** Automated & scheduled fine-tuning jobs (no session limits).

Create a `scripts/train_modal.py` and deploy to [Modal](https://modal.com):

```python
import modal

app = modal.App("finetune-lab")
image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "peft", "bitsandbytes"
)

@app.function(gpu="T4", timeout=3600)
def train():
    import torch
    print(f"GPU: {torch.cuda.get_device_name()}")
    # your training code here
```

```
modal deploy scripts/train_modal.py
modal run scripts/train_modal.py
```

$30/mo free tier. Better for batch jobs than interactive work.

---

## Comparison Table

| Method                | Interactive | Programmatic | Persists?    | Setup     | GPU         |
|-----------------------|-------------|--------------|--------------|-----------|-------------|
| Cloudflare + Jupyter  | ✅ Browser  | ✅ API       | ❌ Per session | 2 clicks  | T4 free    |
| VS Code Tunnel        | ✅ IDE      | ❌           | ❌ Per session | 2 clicks  | T4 free    |
| Drive Sync            | ✅ Colab UI | ❌           | ✅ Drive     | 1 click   | T4 free    |
| GitHub Link           | ✅ Colab UI | ❌           | ✅ GitHub    | 1 click   | T4 free    |
| Modal                 | ❌          | ✅ SDK       | ✅ Deployed  | Sign up   | T4, A100  |
| Kaggle Notebooks      | ✅ Browser  | ❌           | ✅ Kaggle    | Sign up   | T4 x2, P100|
| Lightning AI          | ✅ Studio   | ✅ SDK       | ✅ Persistent| Sign up   | T4 free    |
| HF Spaces (ZeroGPU)   | ✅ Gradio   | ✅ API       | ✅ Persistent| Sign up   | A10G free  |

---

## Quick Decision

```
Want to edit notebooks interactively on Colab with a live connection?
    → Method 1 (Jupyter + Cloudflare) — also works with scripts/colab-client.py

Want a full IDE with terminal + extensions?
    → Method 2 (VS Code Tunnel)

Want zero setup, just open and run?
    → Method 3 (Drive Sync) or 4 (GitHub Link)

Want automated batch jobs without Colab's 2h limit?
    → Method 5 (Modal) or Kaggle / Lightning AI
```
