---
tags:
  - Generative AI
---

## What is a large language model?

A large language model (LLM) is a deep learning model built on the transformer and trained on a massive amount of text to do one job: predict the next token. Given everything so far, what comes next? Get really good at that across trillions of tokens and the model picks up grammar, facts, reasoning patterns, and code along the way.

That's why one LLM can summarize, classify sentiment, answer questions, translate, and write or explain code. It's not a different model for every task.

In the Microsoft world, Microsoft Security Copilot, Copilot Studio, and Azure OpenAI in Microsoft Foundry all sit on top of LLMs. Knowing how the model works underneath explains a lot of why those tools act the way they do.

## How does a model go from nothing to useful?

1. Pre-training: the model reads internet-scale text and learns to predict the next token. What comes out is a foundation model (base model). It knows a lot, but it's not a helpful assistant yet. Ask a base model a question and it might just keep writing more questions. Think of it as a blank slab of marble.
2. Post-training: this is what turns the base model into something you can actually talk to. It usually includes supervised fine-tuning (training on lots of example conversations with good answers) and reinforcement learning like RLHF (reinforcement learning from human feedback), where people rate responses and the model gets rewarded for the ones they prefer. Labs also use AI feedback and automated checks now, not only humans.
3. Your own fine-tuning (optional): companies can fine-tune a model even further on their own examples. I wrote about when that's worth it in [RAG, CAG, and Memory](rag_cag_and_memory.md).

## What does temperature actually change?

Every time the model picks the next token, it has a probability for every token in its vocabulary. Temperature changes how it picks from that list. It's basically how much risk you let the model take on its next word.

- Low temperature (around 0 to 0.3) sticks to the most likely tokens. Answers are more focused and repeatable. This is what you want for KQL, code, or pulling facts out of a document.
- High temperature (around 0.8 and up) gives the less likely tokens more of a chance. Answers get more creative and varied, and also more likely to go off the rails.

In Azure OpenAI, temperature goes from 0 to 2. Microsoft recommends changing either temperature or `top_p` (another sampling setting) but not both.

Two things that tripped me up:

1. Temperature 0 doesn't make the model right, it makes it consistent. It can be consistently wrong.
2. Most reasoning models, like the o-series in Azure OpenAI, don't support temperature at all. You tune them with `reasoning_effort` instead.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/openai/reference-preview-latest)

## What are reasoning models?

Regular LLMs start answering right away. Reasoning models spend extra compute "thinking" first. They generate a chain of thought (breaking the problem into steps, checking their work, backtracking when something doesn't add up) before giving the final answer. OpenAI's o-series, Claude with extended thinking, and DeepSeek R1 all work like this.

The trade-off is cost and time. Those thinking tokens get billed, so a reasoning model is overkill for "what's the KQL operator for contains?" but usually worth it for multi-step debugging or working through an incident timeline. In Azure OpenAI they also use `max_completion_tokens` instead of `max_tokens`.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/foundry/openai/how-to/reasoning)
