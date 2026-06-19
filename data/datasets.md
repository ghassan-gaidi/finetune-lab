# Datasets

Catalogue of datasets used in fine-tuning experiments, with preparation notes.

---

## Dataset Preparation Checklist

- [ ] Check license (Apache 2.0 / MIT / CC-BY preferred for open models)
- [ ] Format to `{"instruction": "...", "output": "..."}` or chat template
- [ ] Split into train/validation
- [ ] Tokenize & check sequence length distribution
- [ ] Upload to HF Hub or mount from Drive

---

## Recommended Datasets

### Instruction Tuning
| Dataset | Size | License | Notes |
|---------|------|---------|-------|
| [OpenHermes 2.5](https://huggingface.co/datasets/teknium/OpenHermes-2.5) | 1M | MIT | Curated, high quality |
| [Capybara](https://huggingface.co/datasets/ldjwas/capybara) | 16K | MIT | Synthetic, conversational |
| [No Robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots) | 10K | Apache-2.0 | Clean DPO/instruction mix |
| [UltraChat 200k](https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k) | 200K | MIT | Multi-turn chat |
| [Tulu 3 SFT](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | 900K | ODC-By | Diverse instructions |

### Code
| Dataset | Size | Notes |
|---------|------|-------|
| [Magicoder-Evol-Instruct](https://huggingface.co/datasets/ise-uiuc/Magicoder_oss_instruct) | 75K | Code generation |
| [CodeAlpaca 20k](https://huggingface.co/datasets/sahil2801/CodeAlpaca-20k) | 20K | Code instructions |

### Preference / Alignment
| Dataset | Size | Notes |
|---------|------|-------|
| [UltraFeedback](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized) | 63K | DPO pairs |
| [Orca DPO Pairs](https://huggingface.co/datasets/Intel/orca_dpo_pairs) | 12K | Academic use |
| [HelpSteer2](https://huggingface.co/datasets/nvidia/HelpSteer2) | 35K | Fine-grained preferences |

---

## Format Templates

### Chat Template (most compatible)
```json
{
  "messages": [
    {"role": "user", "content": "Explain quantum computing in simple terms."},
    {"role": "assistant", "content": "Quantum computing uses qubits that..."}
  ]
}
```

### Instruction-Output (for SFTTrainer)
```json
{
  "instruction": "Explain quantum computing in simple terms.",
  "output": "Quantum computing uses qubits that can be both 0 and 1 simultaneously..."
}
```

### DPO Format
```json
{
  "chosen": "This is the preferred response...",
  "rejected": "This response was rejected...",
  "prompt": "Explain quantum computing."
}
```

---

## Preprocessing with `datasets`

```python
from datasets import load_dataset

dataset = load_dataset("json", data_files="data/mydata.jsonl")

def format_chat(example):
    return {
        "text": tokenizer.apply_chat_template([
            {"role": "user", "content": example["instruction"]},
            {"role": "assistant", "content": example["output"]},
        ], tokenize=False)
    }

dataset = dataset.map(format_chat)
```
