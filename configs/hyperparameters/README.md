# Hyperparameter Configurations

Templated YAML configs for different model sizes and training scenarios.

---

## QLoRA — 7B Model (Colab T4, 16GB VRAM)

```yaml
# configs/hyperparameters/qwen-2.5-7b-qlora.yaml
model:
  name: Qwen/Qwen2.5-7B-Instruct
  load_in_4bit: true
  bnb_4bit_quant_type: nf4
  bnb_4bit_compute_dtype: bfloat16
  use_double_quant: true

lora:
  r: 16
  lora_alpha: 32
  target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
  lora_dropout: 0.05

training:
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  gradient_checkpointing: true
  max_seq_length: 2048
  learning_rate: 2e-4
  lr_scheduler: cosine
  num_train_epochs: 2
  warmup_ratio: 0.03
  logging_steps: 25
  save_steps: 100
  bf16: true
  optim: paged_adamw_8bit
  output_dir: ./outputs
```

---

## QLoRA — 3B Model (Colab T4, comfortable)

```yaml
model:
  name: unsloth/Llama-3.2-3B
  load_in_4bit: true

lora:
  r: 32
  lora_alpha: 64
  target_modules: all
  lora_dropout: 0

training:
  per_device_train_batch_size: 8
  gradient_accumulation_steps: 2
  max_seq_length: 4096
  learning_rate: 5e-4
  num_train_epochs: 3
  bf16: true
  optim: adamw_8bit
```

---

## LoRA — 1.5B Model (Full 16-bit)

```yaml
model:
  name: Qwen/Qwen2.5-1.5B-Instruct
  load_in_4bit: false  # full 16-bit

lora:
  r: 64
  lora_alpha: 128
  target_modules: all

training:
  per_device_train_batch_size: 16
  gradient_accumulation_steps: 1
  max_seq_length: 2048
  learning_rate: 1e-4
  num_train_epochs: 2
  bf16: true
```
