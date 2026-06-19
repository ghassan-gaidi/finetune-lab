# Agentic Datasets — Research Catalog

Curated list of the **best available datasets for training agentic LLMs** —
tool calling, function calling, multi-step reasoning, task completion, and
agent trajectory data. Sourced from Hugging Face Hub (June 2026).

---

## Tier 1 — Hermes Agent Traces (Highest Recommended)

These datasets contain real multi-turn agent conversations with `<think>`
reasoning blocks, `<tool_call>` invocations, and `<tool_response>` results.
**Directly compatible with DeepHermes-3's training format.**

| Dataset | Config | Samples | Downloads | Likes | Size |
|---------|--------|---------|-----------|-------|------|
| [lambda/hermes-agent-reasoning-traces](https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces) | kimi | 7,646 | 3,111 | 363 | ~50 MB |
| lambda/hermes-agent-reasoning-traces | glm-5.1 | 7,055 | — | — | ~45 MB |
| [DJLougen/hermes-agent-traces-filtered](https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered) | — | 3,679 | 1,049 | 33 | ~25 MB |

**Why they're Tier 1:**
- ShareGPT format (`conversations` column) — plug straight into `tokenizer.apply_chat_template()`
- Every sample has `<think>` reasoning → teaches the model to *reason before acting*
- Multi-turn with actual tool responses → teaches error recovery and verification
- The filtered subset (DJLougen) has **10.5× more self-correction** and **3.6× more verification** than the raw traces
- **No API key required to download**

**Schema:**
| Field | Type | Description |
|-------|------|-------------|
| `conversations` | list[dict] | Multi-turn dialogue `{from, value}` |
| `tools` | str | JSON tool definitions available |
| `category` | str | High-level task category |
| `subcategory` | str | Fine-grained task type |
| `task` | str | Original user prompt |

---

## Tier 2 — Function Calling & Tool Use

Focused on teaching the model to format correct tool calls, select parameters,
and handle structured outputs.

| Dataset | Config | Samples | Downloads | Likes |
|---------|--------|---------|-----------|-------|
| [glaiveai/glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) | default | 150,000+ | 53,177 | 514 |
| [NousResearch/hermes-function-calling-v1](https://huggingface.co/datasets/NousResearch/hermes-function-calling-v1) | func_calling | 8,372 | 29,679 | 422 |
| NousResearch/hermes-function-calling-v1 | func_calling_singleturn | 1,620 | — | — |
| NousResearch/hermes-function-calling-v1 | glaive_func_calling | 5,000 | — | — |
| NousResearch/hermes-function-calling-v1 | json_mode_agentic | 3,500 | — | — |
| NousResearch/hermes-function-calling-v1 | json_mode_singleturn | 1,800 | — | — |
| [smolagents/hermes-function-calling-v1-formatted-code-agent](https://huggingface.co/datasets/smolagents/hermes-function-calling-v1-formatted-code-agent) | func_calling | 1,893 | 56 | 3 |

**Details:**
- **glaiveai/glaive-function-calling-v2** — The most downloaded FC dataset. Broad coverage of tools (search, weather, math, databases, APIs). Format: JSON file, need to inspect schema.
- **NousResearch/hermes-function-calling-v1** — Official Hermes FC dataset used to train Hermes 2 Pro. ShareGPT format. Multi-turn with tool responses. Gold standard for FC fine-tuning.
- **smolagents/hermes-function-calling-v1-formatted-code-agent** — HuggingFace smolagents format with `messages` + `chat_template_kwargs` (python_tools, enable_thinking). Reformatted for code-based agents.

---

## Tier 3 — Agentic Instruction & Reasoning

General instruction data with strong agentic / reasoning focus.

| Dataset | Subsets | Samples | Downloads | Likes |
|---------|---------|---------|-----------|-------|
| [microsoft/orca-agentinstruct-1M-v1](https://huggingface.co/datasets/microsoft/orca-agentinstruct-1M-v1) | 15 | 1,073,410 | 3,293 | 465 |
| [zai-org/AgentInstruct](https://huggingface.co/datasets/zai-org/AgentInstruct) | multiple | 250,000+ | 2,043 | 235 |

**Orca-AgentInstruct subsets:**
| Subset | Samples | Topic |
|--------|---------|-------|
| analytical_reasoning | 25,000 | Logical reasoning chains |
| fermi | 25,000 | Fermi estimation (approximation + reasoning) |
| fs_cot_flow | 25,000 | Few-shot chain-of-thought |
| code_ | 100,000 | Code generation + reasoning |
| rag | 50,000 | Retrieval-augmented generation |
| mcq | 99,986 | Multi-choice QA with reasoning |
| open_domain_qa | 272,370 | Open-domain question answering |
| follow_up | 99,054 | Multi-turn conversations |
| brain_teaser | 50,000 | Puzzles and lateral thinking |
| creative_content | 50,000 | Creative writing |
| text_modification | 50,000 | Text editing tasks |
| text_extraction | 50,000 | Information extraction |
| struct2text_flow | 50,000 | Structured data → text |
| rc | 50,000 | Reading comprehension |
| text_classification | 50,000 | Classification tasks |

Licensed under **CDLA-Permissive 2.0** — free for commercial use.

---

## Tier 4 — Complementary (Accuracy & Speed Focus)

| Dataset | Samples | Notes |
|---------|---------|-------|
| [teknium/OpenHermes-2.5](https://huggingface.co/datasets/teknium/OpenHermes-2.5) | 1M | General instruction quality. Good backbone. MIT license. |
| [HuggingFaceH4/ultrachat_200k](https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k) | 200K | Multi-turn chat diversity. MIT. |
| [HuggingFaceH4/no_robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots) | 10K | Clean, human-written. Apache-2.0. Good for polish. |
| [allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | 900K | Broad instruction mixture. ODC-By license. |

---

## Recommended Mix Strategy

For a **small local agentic LLM** (8B, T4-trained):

```
30%  Hermes agent reasoning traces      (Tier 1 — reasoning + tool use)
30%  Function calling data               (Tier 2 — tool dispatch accuracy)
20%  AgentInstruct analytical subsets    (Tier 3 — reasoning depth)
10%  UltraChat / No Robots               (Tier 4 — conversation polish)
10%  Code data                           (Tier 3 — code reasoning)
```

The QLoRA notebook at `notebooks/lora/example_qlora_colab.ipynb` implements
this strategy via the `DATASET_MIX` array.

## Format Reference

### ShareGPT (used by Tiers 1-2)
```json
{
  "conversations": [
    {"from": "system", "value": "You are a helpful assistant."},
    {"from": "human", "value": "Search for the latest news on AI."},
    {"from": "gpt", "value": "<think>I need to use the search tool...</think>\n<tool_call>{\"name\": \"search\", \"arguments\": {\"q\": \"AI news\"}}</tool_call>"},
    {"from": "tool", "value": "<tool_response>{\"results\": [...]}</tool_response>"},
    {"from": "gpt", "value": "Here are the latest AI news stories..."}
  ]
}
```

### OpenAI Messages (some Tier 2-3)
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Loading from Source

```python
from datasets import load_dataset

# Tier 1 — agent reasoning traces
ds = load_dataset("lambda/hermes-agent-reasoning-traces", "kimi", split="train")
ds = load_dataset("lambda/hermes-agent-reasoning-traces", "glm-5.1", split="train")

# Tier 1 — filtered high-quality
ds = load_dataset("DJLougen/hermes-agent-traces-filtered", split="train")

# Tier 2 — function calling
ds = load_dataset("NousResearch/hermes-function-calling-v1", "func_calling", split="train")

# Tier 3 — agent instruct
ds = load_dataset("microsoft/orca-agentinstruct-1M-v1", split="analytical_reasoning")
```
