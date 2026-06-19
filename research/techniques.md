# Fine-Tuning Techniques

Deep dives into the methods used in this lab.

---

## LoRA (Low-Rank Adaptation)

**Paper:** [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

Freezes base model weights and injects trainable rank decomposition matrices into attention layers.

**Key Config:**
```python
from peft import LoraConfig
config = LoraConfig(
    r=16,           # rank — lower = fewer params, r=8-64 typical
    lora_alpha=32,  # scaling factor
    target_modules=["q_proj", "v_proj"],  # which layers to adapt
    lora_dropout=0.05,
    bias="none",
)
```

**Rule of thumb:** `alpha = 2 × r` is a good starting point.

---

## QLoRA (Quantized LoRA)

**Paper:** [QLoRA: Efficient Finetuning of Quantized Language Models](https://arxiv.org/abs/2305.14314)

Combines 4-bit NormalFloat quantization with LoRA. The base model is quantized to 4-bit via NF4, then LoRA adapters are trained in BFloat16.

**Key Config:**
```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,  # saves ~0.5GB
)
```

**VRAM Savings:** ~4x reduction vs 16-bit. A 7B model fits in ~6GB VRAM.

---

## GRPO (Group Relative Policy Optimization)

For reasoning / alignment fine-tuning. Used by DeepSeek-R1. Doesn't need a separate value model — uses group-based advantage estimation.

**Implementation:** `TRL`'s `GRPOTrainer` (v0.15+)

---

## DPO (Direct Preference Optimization)

**Paper:** [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)

Aligns models without reinforcement learning. Uses paired preference data (chosen vs rejected) to directly optimize the policy.

---

## Unsloth Optimizations

[Unsloth](https://github.com/unslothai/unsloth) reimplements attention and linear layers to reduce memory usage and increase throughput.

- **2x speedup** for LoRA/QLoRA training
- **~50% less memory** than standard HF + PEFT
- Drop-in replacement for `AutoModelForCausalLM`

```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, r=16, ...)
```

---

## Scaling Laws & Best Practices

- **Rank vs batch size:** Higher rank (r=32+) benefits from larger batch sizes
- **Learning rate:** 1e-4 for LoRA, 2e-5 for full fine-tuning (starting point)
- **Sequence length:** Longer = more VRAM. On Colab T4 (16GB), 2048 tokens is comfortable for 7B models with QLoRA
- **Gradient checkpointing:** Essential for large models — saves ~30% VRAM at 20% speed cost
- **Mixed precision:** `bf16` preferred over `fp16` for stability

---

## Merging & Exporting

```python
# Merge LoRA weights into base model
merged = model.merge_and_unload()
merged.save_pretrained("./merged-model")
tokenizer.save_pretrained("./merged-model")

# Convert to GGUF (for llama.cpp inference)
# python convert.py ./merged-model --outfile model.gguf
```
