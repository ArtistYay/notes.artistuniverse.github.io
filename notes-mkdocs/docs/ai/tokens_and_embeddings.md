---
tags:
  - Generative AI
---

## What is a token?

Tokens aren't letters, words, or phrases. They're the chunks a LLM breaks text into before it does anything with it. A token can be a whole word ("report"), part of a word ("ham" + "bur" + "ger"), a single character, or punctuation. For typical English text, one token is roughly 4 characters, or about 3/4 of a word.

The chopping up is done by a tokenizer. GPT models use a method called Byte Pair Encoding (BPE). BPE starts with single characters and keeps merging the pairs that show up together the most until it has a vocabulary of common chunks. That's why common words are usually one token while rare words, code, and non-English text get split into more tokens (and cost more).

Every token gets a number (token ID). The model never actually sees your text, only those IDs.

[Documentation | Microsoft Learn](https://learn.microsoft.com/dotnet/ai/conceptual/understanding-tokens)

## Why do tokens cost money?

It comes down to compute. Every token has to run through the model's billions of weights on a GPU, which is a ton of matrix math (multiplying giant grids of numbers). Output tokens are even more work because the model writes its answer one token at a time and runs the whole model again for each new one. On top of that, attention compares tokens to each other, so the longer your input is, the heavier every step gets.

That's why providers charge per token, usually listed per 1 million tokens, and output tokens usually cost more than input tokens. You pay both ways too. Send a 1,000 token prompt, get a 1,000 token answer back, and you're billed for about 2,000.

!!! note "What I got wrong"
    I originally wrote that BPE was the GPU math that makes tokens expensive. BPE is just how the text gets split up, and that part is cheap. The expensive part is running the model on every single token.

[AI Tokens Explained: What They Are and Why They Cost Money - Beginners in AI](https://beginnersinai.org/ai-tokens-explained/)

[Tech in Five - Tokens & Tokenomics - YouTube](https://www.youtube.com/watch?v=PbngY1n4Awc&t=2s)

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/manage-costs) - How Azure OpenAI bills tokens.

## What is an embedding and how is it different from a token?

A token is basically a lookup number for a chunk of text. It doesn't say anything about meaning. An embedding is a list of numbers (a vector) that represents what the text means.

The numbers are laid out so similar meanings land close together in this huge multi-dimensional space. "Cat" and "dog" end up near each other, "laptop" ends up way over somewhere else. You can embed a single word, a sentence, or a whole chunk of a document.

The way I think about it: if a token is your employee ID number, an embedding is where your desk is in the office. People on the same team sit near each other.

To compare two embeddings you usually use cosine similarity, which measures the angle between the two vectors. Smaller angle means more similar meaning. That's what makes semantic search work, where "failed sign-in" can match a doc that says "authentication error" even though none of the words are the same.

This matters for security in two ways:

- Embeddings power vector search and RAG. Azure AI Search, Cosmos DB, Azure SQL, and PostgreSQL (pgvector) can all store and search them.
- Embeddings of sensitive documents are still sensitive data. OWASP calls this out as LLM08:2025 Vector and Embedding Weaknesses, so lock down your vector store like any other database.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/understand-embeddings)
