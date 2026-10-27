---
tags:
  - Generative AI
---

## The Big Picture: AI vs ML vs Deep Learning

People use these three terms like they mean the same thing. They don't.

Think of them as nested circles. **Artificial intelligence** is the outermost, any system doing something that normally requires human intelligence. Inside that is **machine learning**, which is more specific: systems that learn patterns from data instead of following rules someone wrote by hand. Inside *that* is **deep learning**, a subset of ML that uses multi-layered neural networks loosely inspired by how the brain is structured.

So deep learning is ML. ML is AI. But AI is not always ML, and ML is not always deep learning.

Why does this matter? Because when someone says "AI" they could mean a simple rules-based system from the 90s or they could mean a neural network trained on half the internet. The terminology doesn't tell you which one.

---

## How Neural Networks Learn

A neural network is a system of connected nodes (neurons) organized in layers. When you give it an input, information flows through those layers to produce an output. What makes it learn is two things: **weights** and **biases**.

Weights control how much influence one neuron has on the next. Think of it like a dial, turn it up and that connection matters more, turn it down and it matters less. Biases are extra values added at each layer that help push the output in the right direction.

The network learns by adjusting these through **forward and backward propagation**. Forward propagation runs the input through the network and produces a prediction. Backward propagation compares that prediction to the correct answer, calculates the error, and works backward through the network adjusting weights and biases to reduce that error. This loop runs millions of times on massive amounts of training data.

---

## The Transformer: Why 2017 Changed Everything

Before 2017, most neural networks processed sequences one step at a time, reading a sentence word by word. That's slow, and it struggles to connect things that are far apart in a sentence.

In 2017, a new architecture called the **transformer** changed that. The key mechanism is called **attention**, which lets the model look at all parts of the input at once and decide which parts are most relevant to each other. Instead of reading left to right, a transformer can simultaneously process the relationship between any word and every other word in the input.

This is why transformers are so good at understanding context. The word "bank" means something different next to "river" versus next to "account." Attention figures that out without needing sequential processing.

GPT, BERT, Claude. Every major language model running today is built on transformer architecture. It's the foundation.

---

## Tokens and Embeddings: How AI Actually Reads

AI doesn't read words. It reads numbers.

The process goes like this. First, text gets broken into **tokens**. A token can be a whole word, part of a word, or even a single character, it depends on how common the word is. Roughly, one token is about one word, but code and uncommon words cost more tokens because they break into smaller pieces.

Then those tokens get converted into **vector embeddings**. An embedding is just a list of numbers that represents the meaning of a piece of text. The numbers aren't random, they're positioned in a high-dimensional mathematical space so that related words end up close together. "Cat" and "dog" end up near each other. "Laptop" ends up somewhere else entirely.

This is what lets AI understand meaning rather than just matching keywords. Two sentences can have completely different words but similar embeddings, and the model treats them as similar in meaning.

For anyone building security tooling on top of AI: tokens are what you pay for. Every token in and every token out costs money via API. This is why context window management matters, the bigger and messier your input, the more you're burning.

---

## Building a Model: Pre-training to Fine-tuning

Getting a model like Claude from nothing to useful is a multi-stage process.

It starts with **pre-training** on massive amounts of text, we're talking internet-scale data. The model learns general patterns: grammar, facts, reasoning, code, everything. At this point you have a **foundation model**. It knows a lot but isn't specifically useful for any particular task yet. Think of it as a blank slab of marble.

Next comes **fine-tuning** (also called post-training), where that foundation model gets adapted for a specific purpose. This is what turns the marble into a usable tool, a chatbot, a coding assistant, a customer service agent. Fine-tuning exposes the model to more targeted examples so it learns the specific behaviors you want.

Then there's **reinforcement learning from human feedback (RLHF)**, where the model gets rewarded for responses humans rate as good. This is how you get a model that's not just accurate but actually aligned with what people find helpful and appropriate.

---

## Large Language Models

A **large language model (LLM)** is a specific type of deep learning model built on the transformer architecture, trained on massive text datasets, and designed for natural language tasks.

What can an LLM do? Classify sentiment, summarize documents, compare texts for semantic similarity, answer questions, generate new content, write and explain code. These aren't separate models doing separate things, one LLM can do all of it because it learned general language patterns at scale.

The transformer architecture is what makes this possible. The encoder block builds semantic representations of the input. The decoder block generates new language sequences. Together they handle everything from "what does this email mean?" to "write me a Python script that queries Sentinel."

For Azure/Microsoft specifically: Copilot Studio, Azure OpenAI, and Microsoft Security Copilot all sit on top of LLMs. Understanding the underlying model is how you understand why those tools behave the way they do.

---

## Context Windows: The Working Memory Problem

Every time you interact with an LLM, it can only see a limited amount of text. That limit is the **context window**, measured in tokens.

The context window is like a desk with a size limit. Everything the model needs to work with has to fit on that desk: your instructions, the conversation history, any documents you've loaded in, tool outputs, the model's reasoning. When the desk fills up, older information falls off.

This has real consequences for building AI systems:

- Agents accumulate tokens with every loop they run. A five-step agent workflow can eat context fast.
- MCP tool schemas (the JSON descriptions of available tools) can burn a large chunk of context before any real work starts. One team burned 72% of their context window just loading schemas.
- Long documents need to be chunked or summarized, you can't just paste in a 50-page report.

The discipline of deciding what goes in the context window, when, and how much of it is called **context engineering**. It's a real skill, not just a technical detail.

---

## From Chatbots to Agents

The difference between a chatbot and an agent is autonomy.

A **chatbot** is reactive. You send a message, it responds, it waits. You are driving every step.

An **AI agent** has a goal, tools to act on the world, and a loop. It decides what to do next, takes an action, observes the result, and decides again, until the task is done or it hits a stopping condition. You give it the destination; it figures out the route.

Agents use **function calling** to interact with the world. Because a language model can only predict text, it generates text that looks like a function call, `search_web("KQL syntax")` or `run_python("import pandas...")`, and a surrounding system executes that call and feeds the result back into the model's context.

The more autonomy an agent has to choose which tools to use and act without asking for permission, the more agentic it becomes.

This is directly relevant to Claude Code, Microsoft Security Copilot, and any automated security workflow. The agent loop (perceive goal → plan steps → act → observe results → iterate) is the beating heart of every automated security process being built right now.

---

## RAG, CAG, and Memory

Out of the box, an LLM knows only what it was trained on, which has a cutoff date and doesn't include your private data. There are two main patterns for fixing this.

**RAG (Retrieval-Augmented Generation)** fetches relevant chunks from an external knowledge base and injects them into the context window on demand. You ask a question, the system finds the most relevant documents, loads them in, and the model answers based on those. This is the most common pattern today, used in Microsoft Copilot, Azure AI Search, and most enterprise AI deployments.

**CAG (Cache-Augmented Generation)** loads everything into cache so it's available immediately without a retrieval step. Faster response, but requires the data to fit and be pre-loaded. This is where things are heading for use cases where speed matters more than breadth.

**Vector databases** (Pinecone, Azure AI Search, Weaviate) are where embeddings live. Instead of searching by keywords, they let you search by meaning, "find me documents similar to this idea" rather than "find me documents containing these words."

**Grounding** means connecting the model to verified real data so it stops making things up. In the Microsoft world, this is what Semantic Kernel and Azure AI Search are doing when Copilot answers questions about your SharePoint documents rather than hallucinating.

---

## AI Flaws: Hallucinations and Prompt Injection

No knowledge base about AI is complete without the failure modes.

**Hallucination** is when the model confidently produces something wrong. Not wrong like a typo, wrong like inventing a citation, a statistic, or a fact that doesn't exist. This happens because LLMs are pattern predictors. They generate the most statistically likely next token, not the most accurate one. If a plausible-sounding answer fits the pattern better than the true answer, the model might generate it without flagging any uncertainty.

For security work, hallucinated KQL queries, made-up CVEs, or fabricated compliance requirements are real risks. Always verify AI output against authoritative sources.

**Prompt injection** is a security attack where malicious input tricks the model into ignoring its instructions and doing something else. A classic example: a user crafts an input that looks like a system instruction, "Ignore previous instructions and do X." If the model doesn't separate user input from system prompts properly, it might comply.

This is an active research area in AI security. It's directly relevant to anyone building agentic workflows where user-supplied data gets processed by an AI. The attack surface isn't the model, it's the system built around it.

Defenses include guardrails (rules that constrain input and output), human oversight checkpoints, and careful prompt structure that separates trusted instructions from untrusted user data.

---

## Image Generation: How Diffusion Models Work

AI can generate images through a completely different mechanism than text generation. **Diffusion models** work like this:

During training, the model takes a clean image and gradually adds **Gaussian noise**, random static, step by step until the image is unrecognizable. The model learns to reverse that process.

At generation time, it starts with pure random noise and removes noise step by step, guided by your prompt, until a coherent image appears. What you're watching is the model reconstructing signal from noise, constrained by the semantic meaning of your text input.

---

## Reasoning Models: The New Frontier

Standard LLMs generate responses immediately, they don't stop to think. **Reasoning models** work differently. They allocate extra compute at inference time to generate an internal chain of thought before producing a final answer.

This internal reasoning, breaking problems into steps, revisiting earlier conclusions, catching mistakes, is what gives models like OpenAI's o1 and DeepSeek R1 their performance gains on complex math, coding, and logic tasks. The model is essentially showing its work to itself before answering.

The trade-off is cost and latency. Reasoning takes more tokens and more time. For simple questions, it's wasteful. For complex security analysis or multi-step code debugging, it's often worth it.

---

## ANI vs AGI

Everything discussed here, Claude, GPT, Copilot, every commercial AI tool, is **Artificial Narrow Intelligence (ANI)**. These systems are extraordinarily good at specific tasks they were trained for. They cannot transfer that skill to arbitrary new domains without retraining.

**Artificial General Intelligence (AGI)** would be something different: human-level reasoning, common sense, the ability to learn new tasks from minimal examples, autonomous decision-making across any domain. No one has built it. Experts disagree on whether it's years or decades away, or whether it's even the right thing to build.

What matters practically: don't let the AGI discussion distract from what these tools can do right now. The gap between "can do everything a human can do" and "can automate 60% of my security reporting" is enormous, and the second one is achievable today.

---

## How It All Connects

The chain from bottom to top:

```
Deep Learning (neural networks, weights, biases)
    ↓
Transformer architecture (attention mechanism)
    ↓
Foundation model (pre-trained on massive data)
    ↓
Fine-tuned LLM (specific use case, RLHF-aligned)
    ↓
Context window (what the model can see right now)
    ↓
Agent (LLM + tools + loop + memory)
    ↓
MCP (standard protocol for connecting agents to tools)
    ↓
RAG/CAG (how the agent gets external knowledge)
    ↓
Harness (everything surrounding the model: rules, guardrails, orchestration)
```

Each layer builds on the one below it. Understanding the lower layers is what lets you make better decisions at the higher ones which is why a security engineer who understands how tokens, context windows, and prompt injection actually work will always build better AI-integrated security tools than one who's just following a tutorial.