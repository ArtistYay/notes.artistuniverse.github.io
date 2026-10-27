---
tags:
  - Generative AI
---

## What is Generative AI?

AI, machine learning, and deep learning get thrown around like they mean the same thing. They don't. The easiest way I think about it is circles inside circles.

Artificial intelligence (AI) is the big circle. It's any system doing something that normally takes a human brain, and that includes old school rule-based systems where somebody hand wrote every "if this, then that."

Machine learning (ML) sits inside AI. Instead of a person writing the rules, the system learns the patterns from data.

Deep learning sits inside ML. It uses neural networks with a lot of layers, that's where the "deep" comes from.

Generative AI is the part of deep learning that creates new stuff (text, images, code, audio) instead of just labeling or predicting things. ChatGPT, Claude, Copilot, and image generators all live here.

So deep learning is ML and ML is AI, but it doesn't work the other way around. When a vendor says "we use AI" that could be a rules engine from the 90s or a model trained on half the internet, so it's worth asking which one.

## Subcategories

The nav is alphabetical, so here's the order I'd actually read them in:

1. [Neural Networks and Transformers](neural_networks_and_transformers.md)
2. [Tokens and Embeddings](tokens_and_embeddings.md)
3. [Large Language Models](large_language_models.md)
4. [Context Windows](context_windows.md)
5. [From Chatbots to Agents](agents.md)
6. [RAG, CAG, and Memory](rag_cag_and_memory.md)
7. [AI Flaws: Hallucinations and Prompt Injection](ai_flaws.md)
8. [Image Generation](image_generation.md)
9. [ANI vs AGI](ani_vs_agi.md)

## How it all connects

From the bottom up:

```
Deep learning (neural networks, weights, biases)
    ↓
Transformer (self-attention)
    ↓
Foundation model (pre-trained to predict the next token)
    ↓
Post-trained LLM (fine-tuning + RLHF so it acts like an assistant)
    ↓
Context window (everything the model can see in one request)
    ↓
Agent (LLM + tools + a loop)
    ↓
MCP and RAG (how the agent reaches tools and outside knowledge)
    ↓
Harness (everything around the model: rules, guardrails, permissions, orchestration)
```

Each layer sits on the one below it. If you understand how tokens, context windows, and prompt injection work, you'll make better calls building security tooling on top of AI than someone who's only following a tutorial.
